import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import styled from 'styled-components';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { IconButton, SvgIcon } from '@material-ui/core';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
	root: {
		textAlign: 'center',
		width: '100%',
		...theme.typography.button,
		backgroundColor: theme.palette.background.paper,
		padding: theme.spacing(1),
		'& > *': {
			margin: theme.spacing(1),
			width: '25ch'
		}
	},
	heading: {
		marginBottom: 22
	}
}));

const styles = {
	card_content: {
		margin: 'auto',
		width: '100%'
	},
	text_field: {
		margin: 'auto',
		marginBottom: 15
	},
	button: {
		margin: 'auto',
		marginTop: 15
	},
	divider: {
		width: '100%',
		marginTop: 30
	}
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

	const handleClick = (type, index) => {
		console.log(courseInfo);
		let type_symbol;
		if (type === 'Lecture') type_symbol = 'l';
		else if (type === 'Tutorial') type_symbol = 't';
		else type_symbol = 'p';

		let newCourseInfo = { ...courseInfo };
		newCourseInfo[type_symbol].splice(index, 1);
		setCourseInfo(newCourseInfo);
	};

	const handleInfoChange = (e, v, type, index) => {
		// console.log(v,index);
		console.log(courseInfo);
		let type_symbol;
		if (type === 'Lecture') type_symbol = 'l';
		else if (type === 'Tutorial') type_symbol = 't';
		else type_symbol = 'p';
		if (v) {
			let newCourseInfo = courseInfo;
			newCourseInfo[type_symbol][index] = {
				...newCourseInfo[type_symbol][index],
				...v
			};
			setCourseInfo(newCourseInfo);
		}
	};

	const handleAddFaculty = (type) => {
		const newCourseInfo = { ...courseInfo };
		newCourseInfo[type].push(null);
		setCourseInfo(newCourseInfo);
	};

	const addFacutly = (type) => {
		return (
			<Button
				variant="contained"
				color="secondary"
				onClick={() => handleAddFaculty(type)}
				style={{ marginTop: 20 }}
			>
				<Typography>Add Faculty</Typography>
			</Button>
		);
	};

	const getAutoCompleteComp = (data, type, no) => {
		const index = no - 1;
		const sec = no;
		let defaultValue;
		const sections = [];

		if (type === 'Lecture' && courseInfo.l[index]) defaultValue = courseInfo.l[index] || null;
		else if (type === 'Tutorial' && courseInfo.t[index]) defaultValue = courseInfo.t[index] || null;
		else if (type === 'Practical' && courseInfo.p[index]) defaultValue = courseInfo.p[index] || null;

		if (type === 'Lecture') {
			for (let i = 1; i <= courseInfo.l_count; i++) {
				sections.push({ section_number: i.toString() });
			}
		} else if (type === 'Tutorial') {
			for (let i = 1; i <= courseInfo.t_count; i++) {
				sections.push({ section_number: i.toString() });
			}
		} else if (type === 'Practical') {
			for (let i = 1; i <= courseInfo.p_count; i++) {
				sections.push({ section_number: i.toString() });
			}
		}
		return (
			<div style={{ display: 'flex', margin: 'auto', paddingRight: '10px' }}>
				<Autocomplete
					options={data}
					key={data[no]}
					getOptionLabel={(option) => `${option.name} (${option.psrn_or_id})` || null}
					defaultValue={defaultValue}
					style={{ width: '60%', margin: 'auto' }}
					renderInput={(params) => <TextField style={classes.text_field} {...params} label={`${type}`} />}
					onChange={(e, v) => handleInfoChange(e, v, type, index)}
				/>
				<Autocomplete
					options={sections}
					key={data[no]}
					getOptionLabel={(option) => option.section_number.toString() || null}
					defaultValue={defaultValue}
					style={{ width: '20%', margin: 'auto' }}
					renderInput={(params) => <TextField style={classes.text_field} {...params} label={`Sec`} />}
					onChange={(e, v) => handleInfoChange(e, v, type, index)}
				/>
				<IconButton onClick={() => handleClick(type, index)} aria-label="delete">
					<img
						style={{ width: '20px', margin: 'auto' }}
						src="https://img.icons8.com/flat_round/64/000000/delete-sign.png"
					/>
				</IconButton>
			</div>
		);
	};

	const getFacultiesForSections = (type) => {
		const { l, t, p } = courseInfo;
		const data = props.state.faculty_list;
		switch (type) {
			case 'l':
				const lectureFaculties = [];
				for (let i = 1; i <= l.length; i++) {
					lectureFaculties.push(getAutoCompleteComp(data, 'Lecture', i));
				}
				return lectureFaculties;
				break;
			case 't':
				const tutorialFaculties = [];
				for (let i = 1; i <= t.length; i++) {
					tutorialFaculties.push(getAutoCompleteComp(data, 'Tutorial', i));
				}
				return tutorialFaculties;
				break;
			case 'p':
				const practicalFaculties = [];
				for (let i = 1; i <= p.length; i++) {
					practicalFaculties.push(getAutoCompleteComp(data, 'Practical', i));
				}
				return practicalFaculties;
				break;
		}
	};
	return (
		<Card className={classes.root}>
			<CardContent style={styles.card_content}>
				<Typography variant="h6" className={classes.heading}>
					Faculty Info{' '}
					{/* {props.selectedCourse ? ` of ` : null} */}
					<br/>
					{props.selectedCourse ? `${props.selectedCourse.code} - ${props.selectedCourse.name}` : null}
				</Typography>
			</CardContent>
			<CardContent style={styles.card_content}>
				<Typography variant="h5" className={classes.heading}>
					Lectures
				</Typography>
				{getFacultiesForSections('l')}
				{addFacutly('l')}
			</CardContent>
			<CardContent style={styles.card_content}>
				<Typography variant="h5" className={classes.heading}>
					Tutorials
				</Typography>
				{getFacultiesForSections('t')}
				{addFacutly('t')}
			</CardContent>
			<CardContent style={styles.card_content}>
				<Typography variant="h5" className={classes.heading}>
					Practicals
				</Typography>
				{getFacultiesForSections('p')}
				{addFacutly('p')}
			</CardContent>
		</Card>
	);
}
