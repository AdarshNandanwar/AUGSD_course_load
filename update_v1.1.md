# API Updates
1.  /get-data
    - is_active renamed to enable
2.  /get-course-data:
    - 2 more fields added in data:
        ```json
        {
            "data": {
                "enable": false,
                "past_course_strength": null
            }
        }
        ```
    - enable is boolean and past_course_strength is integer
    - null case handle kar lena yaad se
    - add a toggle for enable and a display box for past strength in UI
3.  /submit-data
    - send 1 more value for field named "enable", which is boolean.