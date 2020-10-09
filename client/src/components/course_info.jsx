import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import styled from "styled-components";
import Autocomplete from "@material-ui/lab/Autocomplete";
import Switch from "@material-ui/core/Switch";

const useStyles = makeStyles((theme) => ({
  root: {
    textAlign: "center",
    width: "100%",
    ...theme.typography.button,
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(1),
    "& > *": {
      margin: theme.spacing(1),
      width: "25ch",
    },
  },
  heading: {
    marginBottom: 22,
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
    marginTop: 6,
  },
  button: {
    margin: "auto",
    marginTop: 15,
  },
};

const Form = styled.form`
  display: flex;
  flex-direction: column;
  margin: auto;
  width: 100%;
  justify-content: center;
`;

export default function CourseInfo(props) {
  const classes = useStyles();
  const courseInfo = props.courseInfo;
  const setCourseInfo = props.setCourseInfo;

  const handleInfoChange = (e) => {
    const name = e.target.name;
    let value = e.target.value;
    if (name == "enable") value = e.target.checked;

    const l = props.courseInfo.l;
    const t = props.courseInfo.t;
    const p = props.courseInfo.p;

    if (name == "l_count" && value > l.length) {
      let diff = value - l.length;
      while (diff--) {
        l.push(null);
      }
      // l.length = value;
    }
    if (name == "t_count" && value > t.length) {
      let diff = value - t.length;
      while (diff--) {
        t.push(null);
      }
      // t.length = value;
    }
    if (name == "p_count" && value > p.length) {
      let diff = value - p.length;
      while (diff--) {
        p.push(null);
      }
      // p.length = value;
    }
    // console.log(name, value);
    setCourseInfo({ ...courseInfo, l, t, p, [name]: value });
  };
  const handleIcChange = (e, v) => {
    if (v) setCourseInfo({ ...courseInfo, ic: v.psrn_or_id });
  };
  let defaultIC = props.state.faculty_list.find(
    (faculty) => faculty.psrn_or_id == props.courseInfo.ic
  );
  if (!defaultIC) {
    defaultIC = null;
  }
  return (
    <Card className={classes.root}>
      <CardContent style={styles.card_content}>
        <Typography variant="h6" className={classes.heading}>
          Course Info {/* {props.selectedCourse ? ` of ` : null} */}
          <br />
          {props.selectedCourse
            ? `${props.selectedCourse.code} - ${props.selectedCourse.name}`
            : null}
        </Typography>
        <Form className={classes.root} noValidate>
          <TextField
            inputProps={{ min: 0 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.l_count}
            type="Number"
            name="l_count"
            label="no. of lectures"
            style={styles.text_field}
          />
          <TextField
            inputProps={{ min: 0 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.t_count}
            type="Number"
            name="t_count"
            label="no. of tutorials"
            style={styles.text_field}
          />
          <TextField
            inputProps={{ min: 0 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.p_count}
            type="Number"
            name="p_count"
            label="no. of practicals"
            style={styles.text_field}
          />
          {/* <TextField onChange={(event) => handleInfoChange(event)} value={props.courseInfo.l_count} type="Number" name="l_count" label="no. of faculties for lectures" style={styles.text_field} />
                <TextField onChange={(event) => handleInfoChange(event)} value={props.courseInfo.t_count} type="Number" name="t_count" label="no. of faculties for tutorials" style={styles.text_field}  />
                <TextField onChange={(event) => handleInfoChange(event)} value={props.courseInfo.p_count} type="Number" name="p_count" label="no. of faculties for practicals" style={styles.text_field}  /> */}
          <Autocomplete
            options={props.state.faculty_list}
            getOptionLabel={(option) => `${option.name} (${option.psrn_or_id})`}
            style={styles.text_field}
            // value={defaultIC || { name: '', psrn_or_id: '' }}
            value={defaultIC}
            label="IC"
            required={true}
            renderInput={(params) => (
              <TextField
                style={{ ...styles.text_field, width: "100%" }}
                {...params}
                label={"IC"}
              />
            )}
            onChange={(event, value) => handleIcChange(event, value)}
          />
          <TextField
            inputProps={{ min: 0 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.max_strength_per_l}
            type="Number"
            name="max_strength_per_l"
            label="Max Strength Per Lect"
            style={styles.text_field}
          />
          <TextField
            inputProps={{ min: 0 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.max_strength_per_t}
            type="Number"
            name="max_strength_per_t"
            label="Max Strength Per Tut"
            style={styles.text_field}
          />
          <TextField
            inputProps={{ min: 0 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.max_strength_per_p}
            type="Number"
            name="max_strength_per_p"
            label="Max Strength Per Prac"
            style={styles.text_field}
          />
          <TextField
            inputProps={{ min: -1 }}
            onChange={(event) => handleInfoChange(event)}
            value={props.courseInfo.past_course_strength || -1}
            type="Number"
            name="past_course_strength"
            label="Past course strength"
            disabled
            style={styles.text_field}
          />
          <div>
            <p style={{ marginBottom: -10 }}>Course Active</p>
            <Switch
              checked={props?.courseInfo?.enable || false}
              onChange={(event) => handleInfoChange(event)}
              color="primary"
              name="enable"
              inputProps={{ "aria-label": "primary checkbox" }}
            />
          </div>
        </Form>
      </CardContent>
    </Card>
  );
}
