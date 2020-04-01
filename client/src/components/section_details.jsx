import React from 'react'
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import styled from 'styled-components';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

const useStyles = makeStyles(theme =>({
    root: {
        textAlign: 'center',
        width: '100%',
        ...theme.typography.button,
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(1),
        '& > *': {
            margin: theme.spacing(1),
            width: '25ch',
          },
    },
    heading: {
        marginBottom: 22,
    },
  }));

  const styles = {
    card_content: {
        margin: 'auto',
        width: '100%',
    },
    text_field: {
        margin: 'auto',
        marginBottom: 15,
    },
    button: {
        margin: 'auto',
        marginTop: 15,
    },
    divider: {
        width: '100%',
        marginTop: 30,
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

    const handleInfoChange = (e,v,type,no) => {
        console.log(courseInfo);
        console.log(courseInfo);
        let type_symbol;
        if(type === 'Lecture')
        type_symbol = 'l';
        else if(type === 'Tutorial')
        type_symbol = 't';
        else
        type_symbol = 'p';
        let newCourseInfo = courseInfo;
        newCourseInfo[type_symbol][no] = v.psrn_or_id;
        setCourseInfo(newCourseInfo);
    }

    const getAutoCompleteComp = (data,type,no) => {
        let defaultValue;
        if(type === "Lecture")
        defaultValue = props.courseInfo.l[no];
        else if(type === "Tutorial")
        defaultValue = props.courseInfo.t[no];
        else
        defaultValue = props.courseInfo.p[no];

        return (<Autocomplete
                options={data}
                key={data[no].name}
                getOptionLabel={option => option.name}
                defaultValue={defaultValue}
                style={{ width: '80%', margin: 'auto' }}
                renderInput={params => <TextField style={classes.text_field} {...params} label={`${type} ${no+1}`} />}
                onChange={(e,v) => handleInfoChange(e,v,type,no)}
                />);
    };

    const getFacultiesForSections = (type) => {
        const {l_count,t_count,p_count} = props.courseInfo;
        const data = props.state.faculty_list;
        switch (type) {
            case 'l':
                const lectureFaculties = [];
                for (let i = 0; i < l_count; i++) {
                    lectureFaculties.push(getAutoCompleteComp(data,'Lecture',i))
                }
                return lectureFaculties;
                break;
            case 't':
                const tutorialFaculties = [];
                for (let i = 0; i < t_count; i++) {
                    tutorialFaculties.push(getAutoCompleteComp(data,'Tutorial',i))
                }
                return tutorialFaculties;
                break;
            case 'p':
                const practicalFaculties = [];
                for (let i = 0; i < p_count; i++) {
                    practicalFaculties.push(getAutoCompleteComp(data,'Practical',i))
                }
                return practicalFaculties;
                break;
        }
    }
    return (
        <Card className={classes.root}>
        <CardContent style={styles.card_content}>
            <Typography variant="h5" className={classes.heading} >
                Faculty Info {props.selectedCourse ? `of ${props.selectedCourse}` : null}
            </Typography>
        </CardContent>
        <CardContent style={styles.card_content}>
            <Typography variant="h5" className={classes.heading} >
                Lectures
            </Typography>
            {getFacultiesForSections('l')}
        </CardContent>
        <CardContent style={styles.card_content}>
            <Typography variant="h5" className={classes.heading} >
                Tutorials
            </Typography>
            {getFacultiesForSections('t')}
        </CardContent>
        <CardContent style={styles.card_content}>
            <Typography variant="h5" className={classes.heading} >
                Practicals
            </Typography>
            {getFacultiesForSections('p')}
        </CardContent>
        </Card>
    )
}
