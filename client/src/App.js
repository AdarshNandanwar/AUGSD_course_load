import React, {useState, useEffect} from 'react';
import './App.css';
import NavBar from './components/navbar.jsx'
import CourseList from './components/courses_list.jsx'
import Button from '@material-ui/core/Button';
import CourseInfo from './components/course_info.jsx'
import Typography from '@material-ui/core/Typography';
import SectionInfo from './components/section_details.jsx'
import styled from 'styled-components'
import data from './data'
import axios from 'axios'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const FlexDiv = styled.div`
  display: flex;
  flex-direction: row;
`;

const defaultCourseInfo = {
    l_count:0,
    p_count:0,
    t_count:0,
    course_code: null,
    course_type: null,
    max_strength_per_l: 0,
    max_strength_per_t: 0,
    max_strength_per_p: 0,
    course_code: null,
    course_type: null,
    ic: null,
    l: [],
    t: [],
    p: []
  }

function App() {
  
  const [state, setState] = useState(data.data);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [courseInfo, setCourseInfo] = useState(defaultCourseInfo);

  const getData = async () => {
    const res = await axios.get('/course-load/get-data/');
    setState(res.data.data);
  }

  useEffect(() => {
    getData();
  },[]);

  const [status,setStatus] = useState('');
  const handleSubmit =() => {
    setStatus('Submitting');
    if(courseInfo.course_code == null )
      return setStatus('Please Choose a Course');
    if(courseInfo.ic == undefined || courseInfo.ic == null || courseInfo.ic == '')
      return setStatus('Please Choose IC');
    
    let allFieldsFilled = true;

    courseInfo.l.forEach(faculty => {
      if(!faculty || !faculty.psrn_or_id || !faculty.section_number)
      allFieldsFilled = false;
    });

    courseInfo.t.forEach(faculty => {
      if(!faculty || !faculty.psrn_or_id || !faculty.section_number)
      allFieldsFilled = false;
    });

    courseInfo.p.forEach(faculty => {
      if(!faculty || !faculty.psrn_or_id || !faculty.section_number)
      allFieldsFilled = false;
    });

    if(!allFieldsFilled){
      return setStatus('Please fill all fields or delete extra fields');
    }

    let facultyForEachSection = true;

    for(let i =1; i<= courseInfo.l_count; i++){
      const present = courseInfo.l.some(faculty => faculty.section_number == i);
      if(!present){
        facultyForEachSection = false;
        break;
      }
    }

    for(let i =1; i<= courseInfo.t_count; i++){
      const present = courseInfo.t.some(faculty => faculty.section_number == i);
      if(!present){
        facultyForEachSection = false;
        break;
      }
    }

    for(let i =1; i<= courseInfo.p_count; i++){
      const present = courseInfo.p.some(faculty => faculty.section_number == i);
      if(!present){
        facultyForEachSection = false;
        break;
      }
    }

    if(!facultyForEachSection){
      return setStatus('Please choose atlease a faculty for each section');
    }

    courseInfo.student_count = parseInt(courseInfo.student_count);
    axios.post('/course-load/submit-data/',courseInfo)
    .then(response => setStatus('Submitted'))
    .catch(err => setStatus('Not Submitted'));
  }
  const handleLogout = async () => {
    window.location.href="/accounts/logout";
  }
  const handleDownloadCourseWise = async () => {
    window.location.href="/course-load/download-course-wise";
  }
  const handleDownloadInstructorWise = async () => {
    window.location.href="/course-load/download-instructor-wise";
  }
  const handleFileAdd = async () => {
    window.location.href="/course-load/add-comment/";
  }
  const handleCourseDelete = async () => {
    const course_code = courseInfo.course_code;
    if(course_code){
      try{
        await axios.post('/course-load/clear-course/',{course_code});
      }catch(err){
        console.log(err);
      }finally{
        setCourseInfo({...defaultCourseInfo});
      }
    }
    else
    setStatus('Please choose a course before clearing its data');

    setTimeout(() => {
      setStatus('')
    }, 2000);

  }
  return (
    <div className="App">
      <NavBar handleLogout={handleLogout}>
            <Button variant="contained" color="secondary" onClick={handleDownloadCourseWise} style={{marginBottom: 20, marginLeft: '20px'}}>
              <Typography>
                Download Course-wise
              </Typography>
            </Button>
            <Button variant="contained" color="secondary" onClick={handleDownloadInstructorWise} style={{marginBottom: 20, marginLeft: '20px'}}>
              <Typography>
                Download Instructor-wise
              </Typography>
            </Button>
            <br/>
            <Button variant="contained" color="secondary" onClick={handleFileAdd} style={{marginBottom: 20, marginLeft: '20px'}}>
              <Typography>
                Upload Comment File
              </Typography>
            </Button> 
             <Button variant="contained" color="secondary" onClick={handleCourseDelete} style={{marginBottom: 20, marginLeft: '20px'}}>
              <Typography>
                Clear Course Data
              </Typography>
            </Button>
            <br/>
            <Button variant="contained" size={"large"} color="primary" onClick={handleSubmit} style={{marginBottom: 20, marginLeft: '20px'}}>
              <Typography>
                Submit
              </Typography>
            </Button>
              <br/>
            <Typography style={{color: 'red', fontWeight: 'bold',marginBottom: 10}} >{status}</Typography>
          <FlexDiv>
            <CourseList state={state} setState={setState} setSelectedCourse={setSelectedCourse} courseInfo={courseInfo} setCourseInfo={setCourseInfo}/>
            <CourseInfo state={state} selectedCourse={selectedCourse} courseInfo={courseInfo} setCourseInfo={setCourseInfo}/>
            <SectionInfo courseInfo={courseInfo} setCourseInfo={setCourseInfo} state={state} selectedCourse={selectedCourse} />
          </FlexDiv>
      </NavBar>
    </div>
  );
}

export default App;
