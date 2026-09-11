from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

from data_model import DAYS, DAY_NAMES, PERIODS_BY_SESSION, SESSIONS, SchoolData, Slot

try:
    from ortools.sat.python import cp_model
except ImportError:
    cp_model = None


@dataclass
class Lesson:
    class_id: str
    subject: str
    teacher_ids: List[str]
    day: int
    session: str
    period: int
    assignment_id: str = ''


@dataclass
class TeacherQuality:
    teacher_id: str
    total_periods: int
    days_worked: int
    days_off: int
    gaps: int
    split_days: int
    score: int


@dataclass
class ScheduleResult:
    status: str
    lessons: List[Lesson] = field(default_factory=list)
    quality: Dict[str, TeacherQuality] = field(default_factory=dict)
    objective_value: Optional[float] = None
    messages: List[str] = field(default_factory=list)


class ScheduleError(RuntimeError):
    pass


def precheck(data: SchoolData) -> List[str]:
    errors = []
    teacher_ids = {t.id for t in data.teachers}
    class_ids = {c.id for c in data.classes}

    for a in data.assignments:
        if a.class_id not in class_ids:
            errors.append('{}: lớp {} không tồn tại'.format(a.id, a.class_id))
        for tid in a.teacher_ids:
            if tid not in teacher_ids:
                errors.append('{}: GV {} không tồn tại'.format(a.id, tid))
        if a.periods_per_week <= 0 or a.block_size <= 0:
            errors.append('{}: số tiết không hợp lệ'.format(a.id))
        elif a.periods_per_week % a.block_size:
            errors.append('{}: số tiết không chia hết block'.format(a.id))
        for session in a.allowed_sessions:
            if session not in SESSIONS:
                errors.append('{}: buổi {} không hợp lệ'.format(a.id, session))

    loads = {tid: 0 for tid in teacher_ids}
    for a in data.assignments:
        for tid in a.teacher_ids:
            loads[tid] += a.periods_per_week
    for tid, load in loads.items():
        available = sum(bool(x) for x in data.availability.get(tid, {}).values())
        if load > available:
            errors.append('GV {} cần {} tiết nhưng chỉ có {} slot'.format(tid, load, available))
    return errors


def solve_school(data: SchoolData, time_limit_seconds: int = 60) -> ScheduleResult:
    if cp_model is None:
        raise ScheduleError('Chưa cài OR-Tools. Hãy cài requirements.txt')

    errors = precheck(data)
    if errors:
        return ScheduleResult('INVALID_DATA', messages=errors)

    model = cp_model.CpModel()
    teacher_map = data.teacher_map()

    fixed_class = set()
    fixed_teacher = set()
    for f in data.fixed_lessons:
        fixed_class.add((f.class_id, f.day, f.session, f.period))
        for tid in f.teacher_ids:
            fixed_teacher.add((tid, f.day, f.session, f.period))

    placements = []
    class_slot_vars = {}
    teacher_slot_vars = {}
    assignment_day_vars = {}
    home_p1_vars = {t.id: [] for t in data.teachers}

    for ai, a in enumerate(data.assignments):
        for occ in range(a.occurrences):
            occ_vars = []
            for day in DAYS:
                for session in a.allowed_sessions:
                    ps = PERIODS_BY_SESSION[session]
                    for start in range(len(ps) - a.block_size + 1):
                        block = tuple(ps[start:start + a.block_size])
                        valid = True
                        for p in block:
                            if (a.class_id, day, session, p) in fixed_class:
                                valid = False
                                break
                            for tid in a.teacher_ids:
                                if not data.availability.get(tid, {}).get(Slot(day, session, p).key(), False):
                                    valid = False
                                    break
                                if (tid, day, session, p) in fixed_teacher:
                                    valid = False
                                    break
                            if not valid:
                                break
                        if not valid:
                            continue

                        v = model.NewBoolVar('x_{}_{}_{}_{}_{}'.format(ai, occ, day, session, block[0]))
                        placements.append((ai, occ, day, session, block, v))
                        occ_vars.append(v)
                        assignment_day_vars.setdefault((ai, day), []).append(v)

                        for p in block:
                            class_slot_vars.setdefault((a.class_id, day, session, p), []).append(v)
                            for tid in a.teacher_ids:
                                teacher_slot_vars.setdefault((tid, day, session, p), []).append(v)

                        if session == 'S' and 1 in block:
                            for tid in a.teacher_ids:
                                if teacher_map[tid].homeroom_class == a.class_id:
                                    home_p1_vars[tid].append(v)

            if not occ_vars:
                return ScheduleResult(
                    'INFEASIBLE_PRECHECK',
                    messages=['Không có vị trí hợp lệ cho {} lớp {}'.format(a.subject, a.class_id)],
                )
            model.Add(sum(occ_vars) == 1)

        for day in DAYS:
            vs = assignment_day_vars.get((ai, day), [])
            if vs:
                model.Add(sum(vs) <= a.max_occurrences_per_day)

    for c in data.classes:
        for day in DAYS:
            for session in SESSIONS:
                for p in PERIODS_BY_SESSION[session]:
                    vs = class_slot_vars.get((c.id, day, session, p), [])
                    if vs:
                        model.Add(sum(vs) <= (0 if (c.id, day, session, p) in fixed_class else 1))

    for t in data.teachers:
        for day in DAYS:
            for session in SESSIONS:
                for p in PERIODS_BY_SESSION[session]:
                    vs = teacher_slot_vars.get((t.id, day, session, p), [])
                    if vs:
                        model.Add(sum(vs) <= (0 if (t.id, day, session, p) in fixed_teacher else 1))

    objective = []
    teach = {}
    day_active = {}
    session_active = {}

    for t in data.teachers:
        for day in DAYS:
            daily = []
            for session in SESSIONS:
                session_vars = []
                periods = PERIODS_BY_SESSION[session]
                for p in periods:
                    b = model.NewBoolVar('teach_{}_{}_{}_{}'.format(t.id, day, session, p))
                    vs = teacher_slot_vars.get((t.id, day, session, p), [])
                    if (t.id, day, session, p) in fixed_teacher:
                        model.Add(b == 1)
                    elif vs:
                        model.Add(b == sum(vs))
                    else:
                        model.Add(b == 0)
                    teach[(t.id, day, session, p)] = b
                    daily.append(b)
                    session_vars.append(b)

                active = model.NewBoolVar('session_{}_{}_{}'.format(t.id, day, session))
                model.AddMaxEquality(active, session_vars)
                session_active[(t.id, day, session)] = active

                for idx in range(1, len(periods) - 1):
                    p = periods[idx]
                    before = model.NewBoolVar('before_{}_{}_{}_{}'.format(t.id, day, session, p))
                    after = model.NewBoolVar('after_{}_{}_{}_{}'.format(t.id, day, session, p))
                    model.AddMaxEquality(before, [teach[(t.id, day, session, q)] for q in periods[:idx]])
                    model.AddMaxEquality(after, [teach[(t.id, day, session, q)] for q in periods[idx + 1:]])
                    gap = model.NewBoolVar('gap_{}_{}_{}_{}'.format(t.id, day, session, p))
                    current = teach[(t.id, day, session, p)]
                    model.Add(gap <= before)
                    model.Add(gap <= after)
                    model.Add(gap + current <= 1)
                    model.Add(gap >= before + after - current - 1)
                    objective.append(t.gap_penalty * gap)

            active_day = model.NewBoolVar('day_{}_{}'.format(t.id, day))
            model.AddMaxEquality(active_day, daily)
            day_active[(t.id, day)] = active_day
            objective.append(t.active_day_penalty * active_day)
            model.Add(sum(daily) <= t.max_periods_per_day)

            split = model.NewBoolVar('split_{}_{}'.format(t.id, day))
            am = session_active[(t.id, day, 'S')]
            pm = session_active[(t.id, day, 'C')]
            model.Add(split <= am)
            model.Add(split <= pm)
            model.Add(split >= am + pm - 1)
            objective.append(t.split_day_penalty * split)

        active_count = sum(day_active[(t.id, d)] for d in DAYS)
        extra = model.NewIntVar(0, len(DAYS), 'extra_{}'.format(t.id))
        model.Add(extra >= active_count - t.preferred_max_days)
        objective.append(t.extra_day_penalty * extra)

        if t.homeroom_class:
            hit = model.NewBoolVar('home_p1_{}'.format(t.id))
            if home_p1_vars[t.id]:
                model.AddMaxEquality(hit, home_p1_vars[t.id])
            else:
                model.Add(hit == 0)
            objective.append(-t.homeroom_p1_bonus * hit)

    model.Minimize(sum(objective))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_seconds)
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return ScheduleResult('INFEASIBLE', messages=['Không tìm được TKB thỏa ràng buộc hiện tại'])

    lessons = []
    for f in data.fixed_lessons:
        lessons.append(Lesson(f.class_id, f.subject, list(f.teacher_ids), f.day, f.session, f.period, 'FIXED'))

    for ai, occ, day, session, block, v in placements:
        if solver.Value(v):
            a = data.assignments[ai]
            for p in block:
                lessons.append(Lesson(a.class_id, a.subject, list(a.teacher_ids), day, session, p, a.id))

    lessons.sort(key=lambda x: (x.day, x.session, x.period, x.class_id))
    return ScheduleResult(
        'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE',
        lessons=lessons,
        quality=calculate_quality(data, lessons),
        objective_value=solver.ObjectiveValue(),
        messages=['Đã xếp toàn trường'],
    )


def calculate_quality(data: SchoolData, lessons: List[Lesson]) -> Dict[str, TeacherQuality]:
    out = {}
    for t in data.teachers:
        xs = [x for x in lessons if t.id in x.teacher_ids]
        days = {x.day for x in xs}
        gaps = 0
        split_days = 0
        for day in DAYS:
            dx = [x for x in xs if x.day == day]
            if any(x.session == 'S' for x in dx) and any(x.session == 'C' for x in dx):
                split_days += 1
            for session in SESSIONS:
                periods = sorted({x.period for x in dx if x.session == session})
                if len(periods) >= 2:
                    gaps += max(periods) - min(periods) + 1 - len(periods)
        days_worked = len(days)
        days_off = len(DAYS) - days_worked
        penalty = gaps * 6 + split_days * 4 + max(0, days_worked - t.preferred_max_days) * 15
        if t.preferred_max_days <= 5 and days_off == 0:
            penalty += 20
        out[t.id] = TeacherQuality(t.id, len(xs), days_worked, days_off, gaps, split_days, max(0, 100 - penalty))
    return out


def validate_hard_rules(data: SchoolData, lessons: List[Lesson]) -> List[str]:
    errors = []
    seen_class = set()
    seen_teacher = set()
    by_assignment = {}

    for x in lessons:
        ck = (x.class_id, x.day, x.session, x.period)
        if ck in seen_class:
            errors.append('Trùng lớp {} tại {} {}{}'.format(x.class_id, DAY_NAMES[x.day], x.session, x.period))
        seen_class.add(ck)
        for tid in x.teacher_ids:
            tk = (tid, x.day, x.session, x.period)
            if tk in seen_teacher:
                errors.append('Trùng GV {} tại {} {}{}'.format(tid, DAY_NAMES[x.day], x.session, x.period))
            seen_teacher.add(tk)
        if x.assignment_id != 'FIXED':
            by_assignment.setdefault(x.assignment_id, []).append(x)

    for a in data.assignments:
        xs = by_assignment.get(a.id, [])
        if len(xs) != a.periods_per_week:
            errors.append('{} thiếu/thừa tiết'.format(a.id))
            continue
        if any(x.session not in a.allowed_sessions for x in xs):
            errors.append('{} sai buổi'.format(a.id))
        if a.block_size > 1:
            pos = sorted((x.day, x.session, x.period) for x in xs)
            for i in range(0, len(pos), a.block_size):
                chunk = pos[i:i + a.block_size]
                if len(chunk) != a.block_size:
                    errors.append('{} block thiếu'.format(a.id))
                    continue
                d, s, p = chunk[0]
                if chunk != [(d, s, p + j) for j in range(a.block_size)]:
                    errors.append('{} không liền tiết'.format(a.id))
    return errors
