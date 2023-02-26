import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Link as RouterLink } from 'react-router-dom';
// material
import { Button, Typography } from '@mui/material';
// utils
import axios from '../../../utils/axios';
import { determiteOnlineStatus } from '../../../utils/thermostats';

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

ZoneItem.propTypes = {
  thermostat: PropTypes.object.isRequired
};

export default function ZoneItem({ thermostat }) {
  const [sensorTemp, setSensorTemp] = useState('');
  const [online, setOnline] = useState(false);

  useEffect(() => {
    getThermostatData();
  }, []);

  const getThermostatData = async () => {
    const endPoint = `/api/devices/v2/thermostat/data/${thermostat.serial_num}/`;
    await axios
      .get(endPoint)
      .then((response) => {
        if (response.status === 200 && response.data) {
          setSensorTemp(response.data.tl);
          setOnline(determiteOnlineStatus(response.data.timestamp));
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const formatThermostatName = () => {
    if (thermostat.name.length === 0) {
      return thermostat.serial_num;
    } else return thermostat.name.slice(0, 20);
  };

  const formatThermostatTemp = () => {
    if (online) return `${sensorTemp}°F`;
    else return '--';
  };

  return (
    <Button
      key={thermostat.id}
      variant="outlined"
      fullWidth
      component={RouterLink}
      to="/detail"
      state={thermostat}
      sx={{
        minWidth: '300px',
        paddingX: '2rem',
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
      <Typography variant="span">{formatThermostatName()}</Typography>
      <Typography variant="span">{formatThermostatTemp()}</Typography>
    </Button>
  );
}
