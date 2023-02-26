import React, { useState, useEffect } from 'react';
// material
import { styled } from '@mui/material/styles';
import { Box, Button, Card, Grid, Typography, Slider } from '@mui/material';

import { MIconButton } from '../../@material-extend';
import { Icon } from '@iconify/react';
import closeFill from '@iconify/icons-eva/close-fill';
import { useSnackbar } from 'notistack';

import { Link as RouterLink, useLocation } from 'react-router-dom';
// utils
import axios from '../../../utils/axios';
import { determiteOnlineStatus, getCsrfToken } from '../../../utils/thermostats';

import ThermostatEditDialog from './ThermostatEditDialog';
import ControllerDialog from './ControllerDialog';
import ScheduleEventDialog from './SettingDialog';

// ----------------------------------------------------------------------
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

const RootStyle = styled(Card)({
  maxWidth: '500px',
  padding: '3rem 2rem',
  display: 'flex',
  flexDirection: 'column',
  rowGap: '1.5rem',
  overflow: 'hidden'
});

// ----------------------------------------------------------------------
export default function ZoneDetail() {
  const location = useLocation();
  const thermostat = location.state;

  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const [name, setName] = useState(thermostat.name);
  const [point, setPoint] = useState(thermostat.set_temperature);
  const [sensorTemp, setSensorTemp] = useState(0);
  const [onlineStatus, setOnlineStatus] = useState('offline');
  const [controllerSerial, setControllerSerial] = useState('');

  useEffect(() => {
    getThermostatData();
  }, []);

  const handleName = (value) => {
    setName(value);
  }

  const getThermostatData = async () => {
    const endPoint = `/api/devices/v2/thermostat/data/${thermostat.serial_num}/`;
    await axios
      .get(endPoint)
      .then((response) => {
        if (response.status === 200 && response.data) {
          setControllerSerial(response.data.sn2);
          setSensorTemp(response.data.tl);
          setOnlineStatus(determiteOnlineStatus(response.data.timestamp) ? 'online' : 'offline');
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handlePoint = (e) => {
    setPoint(e.target.value);
  };

  const updateSetPoint = async () => {
    const endPoint = `/api/devices/thermostat/set/`;
    const csrfToken = getCsrfToken();
    await axios
      .post(
        endPoint,
        {
          thermostat_sn: thermostat.serial_num,
          set_temperature: point
        },
        { headers: { 'X-CSRFToken': csrfToken } }
      )
      .then((response) => {
        if (response.status === 200) {
          enqueueSnackbar('Setpoint was successfully set', {
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
      });
  };
  return (
    <RootStyle>
      <Box sx={{ display: 'flex', flexDirection: 'row', columnGap: '3rem', alignItems: 'center' }}>
        <Typography variant="span" sx={{ fontSize: '16px' }}>
          IONIQ Thermostat
        </Typography>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            columnGap: '2px',
            justifyContent: 'flex-start',
            alignItems: 'center'
          }}
        >
          <Typography sx={{ fontWeight: '700', flexGrow: 1 }}>{thermostat.name}</Typography>
          <ThermostatEditDialog thermostat={thermostat} onSubmit={handleName} />
        </Box>
      </Box>
      <Box>
        <Grid container spacing={2}>
          <Grid item xs={6} md={6}>
            <Typography>Setpoint</Typography>
          </Grid>
          <Grid item xs={6} md={6}>
            <Typography>{point}&deg;</Typography>
          </Grid>
          <Grid item xs={12}>
            <Slider
              aria-labelledby="tempature-slider"
              value={point}
              onChange={handlePoint}
              marks={marks}
              min={45}
              max={90}
            />
          </Grid>
        </Grid>
      </Box>
      <Box>
        <Grid container spacing={2}>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <Typography>Linked controller:</Typography>
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <ControllerDialog serial={controllerSerial} />
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <Typography>Sensor temp:</Typography>
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <Typography>{sensorTemp || '--'}&deg;</Typography>
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <Typography>Status:</Typography>
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <Typography>{onlineStatus || '--'}</Typography>
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <Typography>Schedule:</Typography>
          </Grid>
          <Grid item xs={6} md={6} display="flex" alignItems="center">
            <ScheduleEventDialog thermostat={thermostat} />
          </Grid>
        </Grid>
      </Box>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          columnGap: '10px'
        }}
      >
        <Button variant="contained" size="small" onClick={updateSetPoint}>
          Save
        </Button>
        <Button variant="outlined" size="small" component={RouterLink} to="/app">
          Back
        </Button>
      </Box>
    </RootStyle>
  );
}
