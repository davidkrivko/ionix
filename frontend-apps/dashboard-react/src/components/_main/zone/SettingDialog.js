import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
// material
import { styled } from '@mui/material/styles';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  Typography,
  IconButton,
  ToggleButton,
  ToggleButtonGroup,
  Select,
  MenuItem,
  Slider,
  Grid,
  TableContainer,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Paper
} from '@mui/material';
import { MIconButton } from '../../@material-extend';
import { Icon } from '@iconify/react';
import closeFill from '@iconify/icons-eva/close-fill';
import { useSnackbar } from 'notistack';

// utils
import axios from '../../../utils/axios';
import { getCsrfToken } from '../../../utils/thermostats';
// ----------------------------------------------------------------------
const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const weekdayList = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'];
const marks = [
  {
    value: 45
  },
  {
    value: 50
  },
  {
    value: 55
  },
  {
    value: 60
  },
  {
    value: 65
  },
  {
    value: 70
  },
  {
    value: 75
  },
  {
    value: 80
  },
  {
    value: 85
  },
  {
    value: 90
  }
];
function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}
const rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9)
];

const DialogStyle = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2)
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1)
  }
}));
// ----------------------------------------------------------------------

SettingDialog.propTypes = {
  thermostat: PropTypes.object.isRequired
};

export default function SettingDialog({ thermostat }) {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const [open, setOpen] = useState(false);
  const [events, setEvents] = useState([]);
  const [scheduleOptions, setScheduleOptions] = useState([]);
  const [weekday, setWeekday] = useState(null);
  const [time, setTime] = useState('');
  const [point, setPoint] = useState(60);

  useEffect(() => {
    loadEvents();
  }, []);
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const loadEvents = async () => {
    const endPoint = `/api/schedules/thermostats/?device_id=${thermostat.id}`;
    await axios
      .get(endPoint)
      .then((response) => {
        if (response.status === 200) {
          setEvents(response.data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const loadScheduleOptions = async (id) => {
    const endPoint = `/api/schedules/options/${id}/`;
    await axios
      .get(endPoint)
      .then((response) => {
        if (response.status === 200) {
          const options = response.data.map((item) => {
            return {
              value: item.id,
              label: item.checkpoint.substring(11, 16)
            };
          });
          setScheduleOptions(options);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const addEvent = async () => {
    const endPoint = `/api/schedules/thermostats/create/`;
    const csrfToken = getCsrfToken();
    await axios
      .post(
        endPoint,
        {
          schedule: time,
          thermostat: thermostat.id,
          setpoint: point
        },
        { headers: { 'X-CSRFToken': csrfToken } }
      )
      .then((response) => {
        if (response.status === 201) {
          handleReset();
          loadEvents();
          enqueueSnackbar('New schedule event was successfully created.', {
            variant: 'success',
            action: (key) => (
              <MIconButton size="small" onClick={() => closeSnackbar(key)}>
                <Icon icon={closeFill} />
              </MIconButton>
            )
          });
        }
      })
      .catch((error) => {
        console.log(error);
        enqueueSnackbar('Something went wrong 🤖. Please, try again later.', {
          variant: 'error',
          action: (key) => (
            <MIconButton size="small" onClick={() => closeSnackbar(key)}>
              <Icon icon={closeFill} />
            </MIconButton>
          )
        });
      });
  };

  const deleteEvent = async (event_id) => {
    const endPoint = `/api/schedules/thermostats/delete/`;
    const csrfToken = getCsrfToken();
    await axios
      .post(
        endPoint,
        {
          pk: event_id
        },
        { headers: { 'X-CSRFToken': csrfToken } }
      )
      .then((response) => {
        if (response.status === 204) {
          loadEvents();
          enqueueSnackbar('Schedule event was successfully deleted.', {
            variant: 'success',
            action: (key) => (
              <MIconButton size="small" onClick={() => closeSnackbar(key)}>
                <Icon icon={closeFill} />
              </MIconButton>
            )
          });
        }
      })
      .catch((error) => {
        console.log(error);
        enqueueSnackbar('Something went wrong 🤖. Please, try again later.', {
          variant: 'error',
          action: (key) => (
            <MIconButton size="small" onClick={() => closeSnackbar(key)}>
              <Icon icon={closeFill} />
            </MIconButton>
          )
        });
      });
  };

  const handleWeekday = (e) => {
    const id = parseInt(e.target.value);
    if (id !== weekday) {
      setWeekday(parseInt(e.target.value));
      loadScheduleOptions(id);
    }
  };

  const handleTime = (e) => {
    setTime(e.target.value);
  };

  const handleTimeClear = () => {
    setTime('');
  };

  const handlePoint = (e) => {
    setPoint(e.target.value);
  };

  const handleReset = () => {
    setWeekday(null);
    setTime('');
    setPoint(60);
  };
  return (
    <div>
      <Button
        variant="outlined"
        onClick={handleClickOpen}
        sx={{
          paddingX: '1.5rem',
          display: 'flex',
          justifyContent: 'space-evenly',
          columnGap: '15px',
          borderColor: '#1f2937',
          color: '#1f2937',
          '&:hover': {
            backgroundColor: '#1f2937',
            borderColor: '#1f2937',
            color: '#fff'
          }
        }}
      >
        SETTINGS
      </Button>
      <DialogStyle onClose={handleClose} aria-labelledby="customized-dialog-title" open={open}>
        <DialogTitle sx={{ m: 0, p: 2 }}>
          <Typography sx={{ fontSize: '18px', fontWeight: '700' }}>Add New Event</Typography>
          <IconButton
            aria-label="close"
            onClick={handleClose}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
              color: (theme) => theme.palette.grey[500]
            }}
          >
            <Icon icon={closeFill} />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers sx={{ minWidth: '350px' }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10px' }}>
            <Box>
              <Typography gutterBottom fontSize="14px">
                1. Select the day of the week
              </Typography>
              <Box>
                <ToggleButtonGroup
                  color="primary"
                  value={weekday}
                  exclusive
                  onChange={handleWeekday}
                  aria-label="weekday"
                >
                  {weekdayList.map((item, index) => {
                    return (
                      <ToggleButton key={index} value={index + 1}>
                        {item}
                      </ToggleButton>
                    );
                  })}
                </ToggleButtonGroup>
              </Box>
            </Box>
            {weekday ? (
              <Box>
                <Typography gutterBottom fontSize="14px">
                  2. Select available time
                </Typography>
                <Box>
                  <Select
                    labelId="clearable-select-label"
                    id="clearable-select"
                    value={time}
                    onChange={handleTime}
                    displayEmpty
                    autoWidth={false}
                    sx={{
                      '& .MuiSelect-select': { padding: '5px 14px', fontSize: '14px' },
                      '& .MuiSelect-iconOutlined': { display: time ? 'none' : '' },
                      '&.Mui-focused .MuiIconButton-root': { color: 'primary.main' }
                    }}
                    renderValue={(value) => (value ? value : <span>Select a available time</span>)}
                    endAdornment={
                      <IconButton
                        sx={{ visibility: time ? 'visible' : 'hidden' }}
                        onClick={handleTimeClear}
                      >
                        <Icon icon={closeFill} />
                      </IconButton>
                    }
                  >
                    {scheduleOptions.length ? (
                      scheduleOptions.map((item, index) => {
                        return (
                          <MenuItem key={index} value={item.value}>
                            {item.label}
                          </MenuItem>
                        );
                      })
                    ) : (
                      <Typography
                        sx={{
                          textAlign: 'center',
                          padding: '5px 10px',
                          fontSize: '14px',
                          opacity: '0.7'
                        }}
                      >
                        No Options
                      </Typography>
                    )}
                  </Select>
                </Box>
              </Box>
            ) : (
              <></>
            )}
            {time ? (
              <>
                <Box>
                  <Typography gutterBottom fontSize="14px">
                    {`3. Select setpoint for this thermostat ${point} °F`}
                  </Typography>
                  <Box>
                    <Slider
                      aria-labelledby="tempature-slider"
                      value={point}
                      onChange={handlePoint}
                      marks={marks}
                      min={45}
                      max={90}
                    />
                  </Box>
                </Box>
                <Box>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Button variant="contained" size="small" fullWidth onClick={addEvent}>
                        Save
                      </Button>
                    </Grid>
                    <Grid item xs={6}>
                      <Button variant="outlined" size="small" fullWidth onClick={handleReset}>
                        Cancel
                      </Button>
                    </Grid>
                  </Grid>
                </Box>
              </>
            ) : (
              <></>
            )}

            <Box mt={3} mb={3}>
              <Typography variant="h6" mb={1}>
                Scheduled events
              </Typography>
              {events.length ? (
                <TableContainer component={Paper}>
                  <Table sx={{ minWidth: 300 }} aria-label="simple table">
                    <TableBody>
                      {events.map((event, index) => (
                        <TableRow
                          key={index}
                          sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                          <TableCell component="th" scope="row">
                            {weekdays[event.schedule.week_day - 1]}
                          </TableCell>
                          <TableCell align="right">
                            {event.schedule.checkpoint.substring(11, 16)}
                          </TableCell>
                          <TableCell align="right">{event.setpoint} °</TableCell>
                          <TableCell align="center">
                            <Button
                              variant="contained"
                              size="small"
                              color="error"
                              onClick={() => deleteEvent(event.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography variant="span" sx={{ fontSize: '14px', opacity: '0.7' }}>
                  You don't have any scheduled thermostat changes
                </Typography>
              )}
            </Box>
          </Box>
        </DialogContent>
      </DialogStyle>
    </div>
  );
}
