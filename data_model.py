from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

DAYS = [2, 3, 4, 5, 6, 7]
DAY_NAMES = {2: 'Thứ 2', 3: 'Thứ 3', 4: 'Thứ 4', 5: 'Thứ 5', 6: 'Thứ 6', 7: 'Thứ 7'}
SESSIONS = ['S', 'C']
SESSION_NAMES = {'S': 'Sáng', 'C': 'Chiều'}
PERIODS_BY_SESSION = {'S': [1, 2, 3, 4], 'C': [1, 2, 3]}


@dataclass(frozen=True)
class Slot:
    day: int
    session: str
    period: int

    def key(self) -> str:
        return '{}-{}-{}'.format(self.day, self.session, self.period)


@dataclass
class Teacher:
    id: str
    name: str
    code: str
    declared_periods: int = 0
    homeroom_class: Optional[str] = None
    preferred_max_days: int = 5
    max_periods_per_day: int = 7
    gap_penalty: int = 50
    split_day_penalty: int = 35
    extra_day_penalty: int = 180
    active_day_penalty: int = 4
    homeroom_p1_bonus: int = 120
    note: str = ''


@dataclass
class SchoolClass:
    id: str
    name: str


@dataclass
class Assignment:
    id: str
    class_id: str
    subject: str
    teacher_ids: List[str]
    periods_per_week: int
    block_size: int = 1
    allowed_sessions: List[str] = field(default_factory=lambda: ['S', 'C'])
    max_occurrences_per_day: int = 2
    note: str = ''

    @property
    def occurrences(self) -> int:
        if self.periods_per_week % self.block_size != 0:
            raise ValueError(
                '{}: periods_per_week={} không chia hết block_size={}'.format(
                    self.id, self.periods_per_week, self.block_size
                )
            )
        return self.periods_per_week // self.block_size


@dataclass
class FixedLesson:
    class_id: str
    subject: str
    teacher_ids: List[str]
    day: int
    session: str
    period: int
    note: str = ''


@dataclass
class SchoolData:
    teachers: List[Teacher]
    classes: List[SchoolClass]
    assignments: List[Assignment]
    availability: Dict[str, Dict[str, bool]]
    fixed_lessons: List[FixedLesson] = field(default_factory=list)
    registered_teachers: List[str] = field(default_factory=list)
    school_name: str = 'Trường TH-THCS-THPT Nguyễn Thị Minh Khai'
    school_year: str = '2026 - 2027'
    semester: str = 'Học kỳ 1'

    def teacher_map(self) -> Dict[str, Teacher]:
        return {t.id: t for t in self.teachers}

    def class_map(self) -> Dict[str, SchoolClass]:
        return {c.id: c for c in self.classes}

    def assignment_map(self) -> Dict[str, Assignment]:
        return {a.id: a for a in self.assignments}

    def to_dict(self) -> dict:
        return {
            'teachers': [asdict(x) for x in self.teachers],
            'classes': [asdict(x) for x in self.classes],
            'assignments': [asdict(x) for x in self.assignments],
            'availability': self.availability,
            'fixed_lessons': [asdict(x) for x in self.fixed_lessons],
            'registered_teachers': list(self.registered_teachers),
            'school_name': self.school_name,
            'school_year': self.school_year,
            'semester': self.semester,
        }

    @staticmethod
    def from_dict(d: dict) -> 'SchoolData':
        return SchoolData(
            teachers=[Teacher(**x) for x in d.get('teachers', [])],
            classes=[SchoolClass(**x) for x in d.get('classes', [])],
            assignments=[Assignment(**x) for x in d.get('assignments', [])],
            availability=d.get('availability', {}),
            fixed_lessons=[FixedLesson(**x) for x in d.get('fixed_lessons', [])],
            registered_teachers=d.get('registered_teachers', []),
            school_name=d.get('school_name', 'Trường TH-THCS-THPT Nguyễn Thị Minh Khai'),
            school_year=d.get('school_year', '2026 - 2027'),
            semester=d.get('semester', 'Học kỳ 1'),
        )


def all_slots() -> List[Slot]:
    return [
        Slot(day, session, period)
        for day in DAYS
        for session in SESSIONS
        for period in PERIODS_BY_SESSION[session]
    ]


def default_full_availability(teachers: List[Teacher]) -> Dict[str, Dict[str, bool]]:
    slots = all_slots()
    return {t.id: {s.key(): True for s in slots} for t in teachers}
