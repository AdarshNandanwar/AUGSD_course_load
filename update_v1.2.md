# Updates
1. Model
    1. LPU in Course (Both CDC and Ele)
    2. sem in Course (CDC)
    3. system id in PHD/ME in Faculty
    4. ME TA Enum in Faculty
    5. New Table for History {course code, timestamp, l, t, p, str_l, str_t, str_p}
2. Changes in input:
    1. system id in phd scholar sheet
    2. LPU, sem in CDC sheet
    3. LPU in elective sheet
2. Changes in output:
    1. LPU field in 'Time Table' Report
    2. system Id of PHD/ME in 'ERP' Report
3. APIs
    1. new get api for course history [GET req with 1 form field: 'course_code']
    2. get-data API gives sem too
    3. get-data API gives ME TAs too
    4. New Report in given format
    <!-- ![New Output Format](new_format.jpeg) -->
3. Frontend
    1. new format option
    2. course history page template 
4. new input format for past course strength 
5. frontend of history page