import re


def parse_student_info(text: str) -> dict:
    student = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    info_lines = []

    for line in lines:
        if re.match(r'^(Overall Attendance|Subjects)\b', line, re.I):
            break
        info_lines.append(line)

    for line in info_lines:
        if ':' in line or '-' in line:
            parts = re.split(r'\s*[:\-]\s*', line, maxsplit=1)
            if len(parts) == 2:
                key, value = parts
                normalized = key.strip().lower().replace(' ', '')
                if normalized in ('rollno', 'rollnumber', 'roll'):
                    student['rollNo'] = value.strip()
                elif normalized in ('name', 'studentname'):
                    student['name'] = value.strip()
                elif normalized in ('branch', 'department'):
                    student['branch'] = value.strip()
                elif normalized in ('semester', 'sem'):
                    student['semester'] = value.strip()
                elif normalized in ('course', 'program'):
                    student['course'] = value.strip()
                elif normalized in ('year', 'academicyear'):
                    student['year'] = value.strip()

    if 'rollNo' not in student:
        roll_match = re.search(r'roll\s*no\s*[:\-]?\s*(\S+)', text, re.I)
        if roll_match:
            student['rollNo'] = roll_match.group(1).strip()

    if 'name' not in student and info_lines:
        if info_lines[0].lower() in ('welcome', 'welcome!') and len(info_lines) > 1:
            candidate = info_lines[1]
            if not re.search(r'roll\s*no', candidate, re.I):
                student['name'] = candidate
        else:
            if not re.search(r'roll\s*no', info_lines[0], re.I):
                student['name'] = info_lines[0]

    return student


def parse_attendance_text(text: str) -> dict | None:
    overall_match = re.search(r'Overall Attendance\s*([0-9]{1,3})%.*?([0-9]+)\s*present.*?([0-9]+)\s*classes', text, re.S)

    subjects = []
    subject_table_match = re.search(
        r'Subjects\s*-+\s*Subject\s+Present\s+Total\s+Percentage\s*-+(.*?)\n\s*-+\s*$',
        text,
        re.S,
    )

    if overall_match:
        overall_percentage = int(overall_match.group(1))
        present = int(overall_match.group(2))
        total = int(overall_match.group(3))
    else:
        overall_percentage = None
        present = None
        total = None

    if subject_table_match:
        rows_text = subject_table_match.group(1).strip()
        for line in rows_text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 4:
                subjects.append(
                    {
                        'name': parts[0].strip(),
                        'present': int(parts[1]),
                        'total': int(parts[2]),
                        'percentage': int(parts[3].rstrip('%')),
                    }
                )

    if overall_match is None and not subjects:
        return None

    return {
        'student': parse_student_info(text),
        'overall': {
            'percentage': overall_percentage or 0,
            'present': present or 0,
            'total': total or 0,
        },
        'subjects': subjects,
        'rawText': text,
    }
