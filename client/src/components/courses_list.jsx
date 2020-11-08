import React, { useState } from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Typography from "@material-ui/core/Typography";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import axios from "axios";
import courseInfo from "./course_info_data";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
  button: {
    width: "100%",
    margin: "auto",
  },
}));

const styles = {
  card_content: {
    margin: "auto",
    width: "100%",
  },
  text_field: {
    width: "90%",
    margin: "auto",
  },
  button: {
    margin: "auto",
    marginTop: 15,
  },
};

export default function SimpleTabs(props) {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);
  const [extraCDC, setExtraCDC] = React.useState(null);
  const [extraElective, setExtraElective] = React.useState(null);
  const [extraCourseStatus, setExtraCourseStatus] = React.useState(null);

  // get month in ist format
  var currentTime = new Date();
  var currentOffset = currentTime.getTimezoneOffset();
  var ISTOffset = 330; // IST offset UTC +5:30
  var ISTTime = new Date(
    currentTime.getTime() + (ISTOffset + currentOffset) * 60000
  );
  const monthNumber = ISTTime.getMonth();
  const semester = monthNumber == 11 || monthNumber < 5 ? 2 : 1;

  // const handleNewCDC_change = (e, v) => {
  // 	setExtraCDC(v);
  // };
  // const handleNewElective_change = (e, v) => {
  // 	setExtraElective(v);
  // };

  const handleNewCourseChange = (e, v) => {
    const isCDC = props.state.other_cdc_list.includes(v);
    const isElective = props.state.other_elective_list.includes(v);

    if (isCDC) {
      setExtraCDC(v);
    } else if (isElective) {
      setExtraElective(v);
    }
  };
  const CDC = [
    ...props.state.department_cdc_list,
    ...props.state.requested_cdc_list,
  ].filter((course) => course.sem == "sem" + semester);
  const Electives = [
    ...props.state.department_elective_list,
    ...props.state.requested_elective_list,
  ];

  // console.log(CDC, "cdc");
  // console.log(Electives, "electives");

  const sortFunction = (a, b) => {
    return a.code.localeCompare(b.code);
  };

  Electives.sort(sortFunction);
  CDC.sort(sortFunction);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleNewCourseSubmit = async () => {
    setExtraCourseStatus("Adding");
    // console.log(extraCDC,extraElective);
    if (!extraElective && !extraCDC)
      setExtraCourseStatus("Please Select A Course");

    if (extraCDC) {
      try {
        const res = await axios.post("/course-load/request-course-access/", {
          course_code: extraCDC.code,
          course_type: "C",
        });
        setExtraCourseStatus(
          "Course Added. You can select courses in the course section."
        );
      } catch (err) {
        setExtraCourseStatus("There is some error in adding the course");
      }
    }

    if (extraElective) {
      try {
        const res = await axios.post("/course-load/request-course-access/", {
          course_code: extraElective.code,
          course_type: "E",
        });
        setExtraCourseStatus(
          "Course Added. You can select courses in the course section."
        );
      } catch (err) {
        setExtraCourseStatus("There is some error in adding the course");
      }
    }

    const res = await axios.get("/course-load/get-data/");
    props.setState(res.data.data);
  };

  const handleClick = async (course) => {
    props.setSelectedCourse(course);
    let course_type;
    if (value == 0) course_type = "C";
    else course_type = "E";
    props.setCourseInfo({
      ...props.courseInfo,
      course_type,
      course_code: course.code,
    });
    // console.log({course_type,course_code:course.code});
    const res = await axios.post("/course-load/get-course-data/", {
      course_type,
      course_code: course.code,
    });
    // console.log(res);
    // const res = {}
    // res.data = courseInfo;
    // const l = res.data.data.l.map(course => course.psrn_or_id);
    // const t = res.data.data.t.map(course => course.psrn_or_id);
    // const p = res.data.data.p.map(course => course.psrn_or_id);
    // res.data.data.l.length = res.data.data.l_count;
    // res.data.data.t.length = res.data.data.t_count;
    // res.data.data.p.length = res.data.data.p_count;
    const ic = res.data.data.ic.psrn_or_id;
    await props.setCourseInfo({
      l_count: 0,
      p_count: 0,
      t_count: 0,
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
      p: [],
      past_course_strength: 0,
      enable: false,
    });
    // await props.setCourseInfo({...res.data.data,l,t,p,ic });
    await props.setCourseInfo({ ...res.data.data, ic });
    // console.log(props.courseInfo);
    console.log(res.data, "course info");
  };

  const getCourseList = (courses) => {
    const coursesCardItems = courses.map((course) => {
      return (
        <CardActions key={course.code}>
          <Button
            style={
              course.enable ? { fontWeight: "900", fontSize: "1.05rem" } : {}
            }
            className={classes.button}
            value={course}
            onClick={(event) => handleClick(course)}
          >
            {course.code} {`(${course.name})`}
          </Button>
        </CardActions>
      );
    });

    return <Card>{coursesCardItems}</Card>;
  };

  const getEquivalentCourses = () => {
    const courses = props.courseInfo.equivalent_course_list || [];
    const coursesCardItems = courses.map((course) => {
      return (
        // <CardActions key={course.code}>
        // 	<Button
        // 		style={course.is_active ?{ fontWeight:  '900',fontSize: '1.05rem' }:{}}
        // 		className={classes.button}
        // 		value={course}
        // 		onClick={(event) => handleClick(course)}
        // 	>
        // 		{course.code} {`(${course.name})`}
        // 	</Button>
        // </CardActions>

        <CardActions key={course.code}>{course.code}</CardActions>
      );
    });

    return <Card>{coursesCardItems}</Card>;
  };
  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="simple tabs example"
        >
          <Tab label="CDC" {...a11yProps(0)} />
          <Tab label="Electives" {...a11yProps(1)} />
          <Tab label="ADD" {...a11yProps(2)} />
          <Tab label="Equivalent Courses" {...a11yProps(3)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {getCourseList(CDC)}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {getCourseList(Electives)}
      </TabPanel>
      <TabPanel value={value} index={2}>
        {/* <Autocomplete
					options={props.state.other_cdc_list.sort(sortFunction)}
					getOptionLabel={(option) => `${option.code} (${option.name})`}
					style={styles.text_field}
					label="Other Department's CDC"
					required={true}
					renderInput={(params) => (
						<TextField
							style={{ ...styles.text_field, width: '100%' }}
							{...params}
							label={"Other Department's CDC"}
						/>
					)}
					onChange={(event, value) => handleNewCDC_change(event, value)}
				/>
				<Autocomplete
					options={props.state.other_elective_list.sort(sortFunction)}
					getOptionLabel={(option) => `${option.code} (${option.name})`}
					style={styles.text_field}
					label="Other Department's Electives"
					required={true}
					renderInput={(params) => (
						<TextField
							style={{ ...styles.text_field, width: '100%' }}
							{...params}
							label={"Other Department's Electives"}
						/>
					)}
					onChange={(event, value) => handleNewElective_change(event, value)}
				/> */}
        <Autocomplete
          options={[
            ...props.state.other_cdc_list,
            ...props.state.other_elective_list,
          ].sort(sortFunction)}
          getOptionLabel={(option) => `${option.code} (${option.name})`}
          style={styles.text_field}
          label="Other Department's Courses"
          required={true}
          renderInput={(params) => (
            <TextField
              style={{ ...styles.text_field, width: "100%" }}
              {...params}
              label={"Other Department's Courses"}
            />
          )}
          onChange={(event, value) => handleNewCourseChange(event, value)}
        />
        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleNewCourseSubmit()}
          style={{ marginBottom: 20, marginTop: 20 }}
        >
          <Typography>ADD</Typography>
        </Button>
        <Typography
          style={{ color: "red", fontWeight: "bold", marginBottom: 10 }}
        >
          {extraCourseStatus}
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={3}>
        {getEquivalentCourses()}
      </TabPanel>
    </div>
  );
}
