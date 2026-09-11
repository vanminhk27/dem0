from __future__ import annotations

from data_model import Assignment, FixedLesson, SchoolClass, SchoolData, Teacher, default_full_availability

_TEACHERS = r"""
GV01|T-Q.Anh|Lê Quang Anh|27||5|7|50|35|180|4|120|Tin (12A1, 12A2, 12A4, 12A5, 12A6) + Toán (11A1, 12A5, 12A6)
GV02|Su-Anh|Nguyễn Việt Hồng Anh|8||3|7|65|35|230|6|120|Sử (10A1, 10A2, 10A3, 10A4)
GV03|QP-Bằng|Phan Thị Bằng|14||4|7|65|35|230|6|120|GDQP (12A1, 12A2, 12A3, 12A4, 12A5, 12A6, 12A7)
GV04|T-Chân|Nguyễn Xuân Chân|13|11A3|4|7|65|35|230|6|160|Toán (11A2, 11A3)
GV05|Su-Dần|Nguyễn Văn Dần|5||3|7|65|35|230|6|120|Sử (11A1, 11A2, 11A3, 12A4)
GV06|V-Hà|Hoàng Thị Hà|29||5|7|50|35|180|4|120|GDĐP (12A4, 12A5) + Văn (10A2, 10A4, 11A2, 12A4, 12A5)
GV07|TD-Hải|Tô Đắc Hải|28||5|7|50|35|180|4|120|TD (10A1, 10A2, 10A3, 10A4, 11A1, 11A2, 11A3, 12A1, 12A2, 12A3, 12A4, 12A5, 12A6, 12A7)
GV08|A-Hạnh|Đào Thị Mỹ Hạnh|13||4|7|65|35|230|6|120|Anh (10A4, 12A1, 12A2, 12A4)
GV09|Su_VHằng|Vũ Thị Hằng|5||3|7|65|35|230|6|120|Sử (12A6, 12A7)
GV10|Su-Huệ|Trần Thị Huệ|8||3|7|65|35|230|6|120|Sử (12A1, 12A2, 12A3, 12A5)
GV11|Vo-Huỳnh|Nguyễn Huỳnh|6||3|7|65|35|230|6|120|Vo (11A1, 11A2, 11A3)
GV12|V-Lài|Nguyễn Thị Hương Lài|31||5|7|50|35|180|4|120|GDĐP (12A1, 12A2, 12A3) + Văn (11A1, 11A3, 12A1, 12A2, 12A3)
GV13|Đ-Loan|Nguyễn Phương Loan|6||3|7|65|35|230|6|120|Địa (12A3, 12A4)
GV14|Tin-Minh|Nguyễn Văn Minh|25||5|7|75|45|300|4|120|Stem (10A1, 10A2, 10A3, 10A4, 11A1, 11A2, 11A3) + Tin (10A1, 10A2, 10A3, 10A4, 11A1, 11A2, 11A3, 12A3, 12A7)
GV15|A-C.Nga|Cao Phạm Tuyết Nga|14||4|7|65|35|230|6|120|Anh (10A2, 10A3, 12A3, 12A6)
GV16|A-P.Nga|Phạm Thị Nga|15||4|7|65|35|230|6|120|Anh (11A2, 11A3, 12A5, 12A7)
GV17|T-TNgân|Nguyễn Thị Tuyết Ngân|17||4|7|50|35|180|4|120|Toán (10A3, 12A2, 12A4)
GV18|T-Nhâm|Nguyễn Thị Nhâm|17||4|7|50|35|180|4|120|Toán (10A2, 12A1, 12A3)
GV19|A-Nhu|Lương Thị Nhu|19||5|7|50|35|180|4|120|Anh (10A1, 11A1) + HĐTN (11A1, 11A2, 11A3, 12A2, 12A3, 12A4, 12A5)
GV20|QP-Quyết|Nguyễn Trọng Quyết|7||3|7|65|35|230|6|120|GDQP (10A1, 10A2, 10A3, 10A4, 11A1, 11A2, 11A3)
GV21|H- Quỳnh|Nguyễn Thị Thảo Quỳnh|17||4|7|50|35|180|4|120|HĐTN (12A1, 12A7) + Hoá (10A1, 10A3, 11A3, 12A1, 12A6)
GV22|Đ-Tân|Trần Duy Tân|23||5|7|50|35|180|4|120|Địa (10A3, 10A4, 11A1, 11A3, 12A6) + GDĐP (10A3, 10A4, 11A1, 11A3) + HĐTN (10A1, 10A2, 10A3, 10A4, 12A6)
GV23|H-Thịnh|Nguyễn Văn Thịnh|3||3|7|65|35|230|6|120|Hoá (12A2)
GV24|Đ-Thỏa|Đoàn Thị Thỏa|17||4|7|50|35|180|4|120|Địa (10A1, 10A2, 11A2, 12A5, 12A7) + GDĐP (10A1, 10A2, 11A2)
GV25|Vo-Tiên|Lê Ngọc Thủy|8||3|7|65|35|230|6|120|Vo (10A1, 10A2, 10A3, 10A4)
GV26|Si-Tiến|Nguyễn Hồng Tiến|9||3|7|65|35|230|6|120|Sinh (12A1, 12A2, 12A5)
GV27|V-Trang|Trần Thị Trang|22||5|7|50|35|180|4|120|GDĐP (12A6, 12A7) + Văn (10A1, 10A3, 12A6, 12A7)
GV28|KT-Tuyền|Nguyễn Thị Thanh Tuyền|16||4|7|50|35|180|4|120|KTPL (10A2, 10A3, 10A4, 11A1, 11A2, 11A3, 12A3, 12A4, 12A5, 12A6, 12A7)
GV29|L-Tuyển|La Thị Mỹ Tuyển|23||5|7|50|35|180|4|120|Lý (10A1, 10A2, 10A4, 11A1, 11A2, 12A1, 12A2, 12A3, 12A4, 12A7)
GV30|T-Xuân|Nguyễn Thị Thanh Xuân|17||4|7|50|35|180|4|120|Toán (10A1, 10A4, 12A7)
""".strip()

_ASSIGNMENTS = r"""
A001|10A1|Anh|GV19|4|1|S,C|1|
A002|10A1|GDQP|GV20|1|1|S,C|1|
A003|10A1|GDĐP|GV24|1|1|S,C|1|
A004|10A1|Hoá|GV21|3|1|S,C|1|
A005|10A1|HĐTN|GV22|1|1|S,C|1|
A006|10A1|Lý|GV29|3|1|S,C|1|
A007|10A1|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A008|10A1|Sử|GV02|1|1|S,C|1|
A009|10A1|TD|GV07|2|1|S,C|2|
A010|10A1|Tin|GV14|2|1|S,C|1|
A011|10A1|Toán|GV30|5|1|S,C|2|
A012|10A1|Võ|GV25|2|2|C|1|
A013|10A1|Văn|GV27|5|1|S,C|2|
A014|10A1|Địa|GV24|2|1|S,C|1|
A015|10A2|Anh|GV15|4|1|S,C|2|
A016|10A2|GDQP|GV20|1|1|S,C|1|
A017|10A2|GDĐP|GV24|1|1|S,C|1|
A018|10A2|HĐTN|GV22|1|1|S,C|1|
A019|10A2|KTPL|GV28|1|1|S,C|1|
A020|10A2|Lý|GV29|2|1|S,C|1|
A021|10A2|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A022|10A2|Sử|GV02|2|1|S,C|1|
A023|10A2|TD|GV07|2|1|S,C|1|
A024|10A2|Tin|GV14|2|1|S,C|1|
A025|10A2|Toán|GV18|6|1|S,C|3|
A026|10A2|Võ|GV25|2|2|C|1|
A027|10A2|Văn|GV06|5|1|S,C|1|
A028|10A2|Địa|GV24|3|1|S,C|1|
A029|10A3|Anh|GV15|4|1|S,C|2|
A030|10A3|GDQP|GV20|1|1|S,C|1|
A031|10A3|GDĐP|GV22|1|1|S,C|1|
A032|10A3|Hoá|GV21|2|1|S,C|1|
A033|10A3|HĐTN|GV22|1|1|S,C|1|
A034|10A3|KTPL|GV28|1|1|S,C|1|
A035|10A3|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A036|10A3|Sử|GV02|3|1|S,C|1|
A037|10A3|TD|GV07|2|1|S,C|1|
A038|10A3|Tin|GV14|2|1|S,C|1|
A039|10A3|Toán|GV17|6|1|S,C|3|
A040|10A3|Võ|GV25|2|2|C|1|
A041|10A3|Văn|GV27|5|1|S,C|2|
A042|10A3|Địa|GV22|2|1|S,C|2|
A043|10A4|Anh|GV08|4|1|S,C|1|
A044|10A4|GDQP|GV20|1|1|S,C|1|
A045|10A4|GDĐP|GV22|1|1|S,C|1|
A046|10A4|HĐTN|GV22|1|1|S,C|1|
A047|10A4|KTPL|GV28|1|1|S,C|1|
A048|10A4|Lý|GV29|2|1|S,C|1|
A049|10A4|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A050|10A4|Sử|GV02|2|1|S,C|1|
A051|10A4|TD|GV07|2|1|S,C|1|
A052|10A4|Tin|GV14|2|1|S,C|1|
A053|10A4|Toán|GV30|6|1|S,C|3|
A054|10A4|Võ|GV25|2|2|C|1|
A055|10A4|Văn|GV06|5|1|S,C|2|
A056|10A4|Địa|GV22|3|1|S,C|2|
A057|11A1|Anh|GV19|4|1|S,C|2|
A058|11A1|GDQP|GV20|1|1|S,C|1|
A059|11A1|GDĐP|GV22|1|1|S,C|1|
A060|11A1|HĐTN|GV19|1|1|S,C|1|
A061|11A1|KTPL|GV28|1|1|S,C|1|
A062|11A1|Lý|GV29|2|1|S,C|2|
A063|11A1|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A064|11A1|Sử|GV05|1|1|S,C|1|
A065|11A1|TD|GV07|2|1|S,C|1|
A066|11A1|Tin|GV14|2|1|S,C|1|
A067|11A1|Toán|GV01|6|1|S,C|2|
A068|11A1|Võ|GV11|2|2|C|1|
A069|11A1|Văn|GV12|6|1|S,C|2|
A070|11A1|Địa|GV22|3|1|S,C|2|
A071|11A2|Anh|GV16|4|1|S,C|1|
A072|11A2|GDQP|GV20|1|1|S,C|1|
A073|11A2|GDĐP|GV24|1|1|S,C|1|
A074|11A2|HĐTN|GV19|1|1|S,C|1|
A075|11A2|KTPL|GV28|1|1|S,C|1|
A076|11A2|Lý|GV29|2|1|S,C|1|
A077|11A2|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A078|11A2|Sử|GV05|1|1|S,C|1|
A079|11A2|TD|GV07|2|1|S,C|1|
A080|11A2|Tin|GV14|2|1|S,C|2|
A081|11A2|Toán|GV04|6|1|S,C|2|
A082|11A2|Võ|GV11|2|2|C|1|
A083|11A2|Văn|GV06|6|1|S,C|3|
A084|11A2|Địa|GV24|3|1|S,C|1|
A085|11A3|Anh|GV16|4|1|S,C|2|
A086|11A3|GDQP|GV20|1|1|S,C|1|
A087|11A3|GDĐP|GV22|1|1|S,C|1|
A088|11A3|Hoá|GV21|2|1|S,C|1|
A089|11A3|HĐTN|GV19|1|1|S,C|1|
A090|11A3|KTPL|GV28|1|1|S,C|1|
A091|11A3|STEM|GV14,GV04|1|1|C|1|STEM đồng giảng Minh + Chân theo cấu hình hiện tại.
A092|11A3|Sử|GV05|1|1|S,C|1|
A093|11A3|TD|GV07|2|1|S,C|1|
A094|11A3|Tin|GV14|2|1|S,C|2|
A095|11A3|Toán|GV04|7|1|S,C|2|
A096|11A3|Võ|GV11|2|2|C|1|
A097|11A3|Văn|GV12|6|1|S,C|2|
A098|11A3|Địa|GV22|2|1|S,C|1|
A099|12A1|Anh|GV08|3|1|S,C|2|
A100|12A1|GDQP|GV03|2|1|S,C|1|
A101|12A1|GDĐP|GV12|1|1|S,C|1|
A102|12A1|Hoá|GV21|3|1|S,C|2|
A103|12A1|HĐTN|GV21|2|1|S,C|2|
A104|12A1|Lý|GV29|3|1|S,C|1|
A105|12A1|Sinh|GV26|3|1|S,C|2|
A106|12A1|Sử|GV10|2|1|S,C|1|
A107|12A1|TD|GV07|2|1|S,C|1|
A108|12A1|Tin|GV01|2|1|S,C|1|
A109|12A1|Toán|GV18|5|1|S,C|2|
A110|12A1|Văn|GV12|5|1|S,C|2|
A111|12A2|Anh|GV08|3|1|S,C|1|
A112|12A2|GDQP|GV03|2|1|S,C|1|
A113|12A2|GDĐP|GV12|1|1|S,C|1|
A114|12A2|Hoá|GV23|3|1|S,C|2|
A115|12A2|HĐTN|GV19|2|1|S,C|1|
A116|12A2|Lý|GV29|3|1|S,C|1|
A117|12A2|Sinh|GV26|3|1|S,C|1|
A118|12A2|Sử|GV10|2|1|S,C|1|
A119|12A2|TD|GV07|2|1|S,C|1|
A120|12A2|Tin|GV01|2|1|S,C|1|
A121|12A2|Toán|GV17|5|1|S,C|2|
A122|12A2|Văn|GV12|5|1|S,C|2|
A123|12A3|Anh|GV15|3|1|S,C|2|
A124|12A3|GDQP|GV03|2|1|S,C|1|
A125|12A3|GDĐP|GV12|1|1|S,C|1|
A126|12A3|HĐTN|GV19|2|1|S,C|1|
A127|12A3|KTPL|GV28|2|1|S,C|1|
A128|12A3|Lý|GV29|2|1|S,C|1|
A129|12A3|Sử|GV10|2|1|S,C|1|
A130|12A3|TD|GV07|2|1|S,C|1|
A131|12A3|Tin|GV14|2|1|S,C|1|
A132|12A3|Toán|GV18|6|1|S,C|3|
A133|12A3|Văn|GV12|6|1|S,C|2|
A134|12A3|Địa|GV13|3|1|S,C|2|
A135|12A4|Anh|GV08|3|1|S,C|2|
A136|12A4|GDQP|GV03|2|1|S,C|2|
A137|12A4|GDĐP|GV06|1|1|S,C|1|
A138|12A4|HĐTN|GV19|2|1|S,C|1|
A139|12A4|KTPL|GV28|2|1|S,C|1|
A140|12A4|Lý|GV29|2|1|S,C|1|
A141|12A4|Sử|GV05|2|1|S,C|2|
A142|12A4|TD|GV07|2|1|S,C|1|
A143|12A4|Tin|GV01|2|1|S,C|1|
A144|12A4|Toán|GV17|6|1|S,C|2|
A145|12A4|Văn|GV06|6|1|S,C|2|
A146|12A4|Địa|GV13|3|1|S,C|2|
A147|12A5|Anh|GV16|3|1|S,C|1|
A148|12A5|GDQP|GV03|2|1|S,C|1|
A149|12A5|GDĐP|GV06|1|1|S,C|1|
A150|12A5|HĐTN|GV19|2|1|S,C|1|
A151|12A5|KTPL|GV28|2|1|S,C|1|
A152|12A5|Sinh|GV26|3|1|S,C|2|
A153|12A5|Sử|GV10|2|1|S,C|1|
A154|12A5|TD|GV07|2|1|S,C|1|
A155|12A5|Tin|GV01|2|1|S,C|1|
A156|12A5|Toán|GV01|6|1|S,C|2|
A157|12A5|Văn|GV06|5|1|S,C|2|
A158|12A5|Địa|GV24|3|1|S,C|2|
A159|12A6|Anh|GV15|3|1|S,C|1|
A160|12A6|GDQP|GV03|2|1|S,C|1|
A161|12A6|GDĐP|GV27|1|1|S,C|1|
A162|12A6|Hoá|GV21|3|1|S,C|1|
A163|12A6|HĐTN|GV22|2|1|S,C|1|
A164|12A6|KTPL|GV28|2|1|S,C|2|
A165|12A6|Sử|GV09|3|1|S,C|2|
A166|12A6|TD|GV07|2|1|S,C|1|
A167|12A6|Tin|GV01|2|1|S,C|1|
A168|12A6|Toán|GV01|5|1|S,C|2|
A169|12A6|Văn|GV27|5|1|S,C|2|
A170|12A6|Địa|GV22|3|1|S,C|1|
A171|12A7|Anh|GV16|4|1|S,C|2|
A172|12A7|GDQP|GV03|2|1|S,C|1|
A173|12A7|GDĐP|GV27|1|1|S,C|1|
A174|12A7|HĐTN|GV21|2|1|S,C|1|
A175|12A7|KTPL|GV28|2|1|S,C|2|
A176|12A7|Lý|GV29|2|1|S,C|1|
A177|12A7|Sử|GV09|2|1|S,C|1|
A178|12A7|TD|GV07|2|1|S,C|1|
A179|12A7|Tin|GV14|2|1|S,C|1|
A180|12A7|Toán|GV30|6|1|S,C|3|
A181|12A7|Văn|GV27|5|1|S,C|2|
A182|12A7|Địa|GV24|3|1|S,C|2|
""".strip()

_CLASS_IDS = "10A1 10A2 10A3 10A4 11A1 11A2 11A3 12A1 12A2 12A3 12A4 12A5 12A6 12A7".split()


def _teachers():
    out = []
    for line in _TEACHERS.splitlines():
        parts = line.split("|", 12)
        tid, code, name = parts[0], parts[1], parts[2]
        out.append(Teacher(
            id=tid,
            code=code,
            name=name,
            declared_periods=int(parts[3]),
            homeroom_class=parts[4] or None,
            preferred_max_days=int(parts[5]),
            max_periods_per_day=int(parts[6]),
            gap_penalty=int(parts[7]),
            split_day_penalty=int(parts[8]),
            extra_day_penalty=int(parts[9]),
            active_day_penalty=int(parts[10]),
            homeroom_p1_bonus=int(parts[11]),
            note=parts[12],
        ))
    return out


def _assignments():
    out = []
    for line in _ASSIGNMENTS.splitlines():
        parts = line.split("|", 8)
        out.append(Assignment(
            id=parts[0],
            class_id=parts[1],
            subject=parts[2],
            teacher_ids=parts[3].split(","),
            periods_per_week=int(parts[4]),
            block_size=int(parts[5]),
            allowed_sessions=parts[6].split(","),
            max_occurrences_per_day=int(parts[7]),
            note=parts[8],
        ))
    return out


def build_school_data() -> SchoolData:
    teachers = _teachers()
    classes = [SchoolClass(id=x, name=x) for x in _CLASS_IDS]
    assignments = _assignments()
    fixed_lessons = []
    for class_id in _CLASS_IDS:
        fixed_lessons.append(FixedLesson(
            class_id=class_id, subject="HĐTN", teacher_ids=[],
            day=2, session="S", period=1,
            note="Tiết HĐTN chung theo TKB mẫu",
        ))
        fixed_lessons.append(FixedLesson(
            class_id=class_id, subject="HĐTN", teacher_ids=[],
            day=6, session="C", period=3,
            note="Tiết HĐTN chung theo TKB mẫu",
        ))
    availability = default_full_availability(teachers)
    return SchoolData(
        teachers=teachers,
        classes=classes,
        assignments=assignments,
        availability=availability,
        fixed_lessons=fixed_lessons,
        registered_teachers=[],
    )
