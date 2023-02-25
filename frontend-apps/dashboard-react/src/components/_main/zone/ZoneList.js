import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
// material
import { Box, Button, OutlinedInput } from '@mui/material';

import ZoneItem from './ZoneItem';
// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

ZoneList.propTypes = {
  zone: PropTypes.object.isRequired,
  index: PropTypes.number
};

export default function ZoneList({ zone, index }) {
  const [edit, setEdit] = useState(false);
  const [name, setName] = useState(zone.name);

  const handleName = (e) => {
    setName(e.target.value);
  };
  return (
    <Box
      sx={{
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        rowGap: '5px'
      }}
    >
      {/* <Typography variant="body1" fontWeight="bold">
        {zone.name}
      </Typography> */}
      {edit ? (
        <OutlinedInput
          value={name}
          onChange={(e) => handleName(e)}
          sx={{
            '& input': {
              padding: '7px 14px'
            }
          }}
        />
      ) : (
        <Button
          variant="text"
          onClick={() => setEdit(true)}
          sx={{
            fontSize: '16px',
            color: '#000',
            padding: 0,
            justifyContent: 'flex-start',
            '&:hover': { backgroundColor: '#fff', boxShadow: 'none' }
          }}
        >
          {zone.name}
        </Button>
      )}

      <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10px' }}>
        {zone.thermostats.map((thermostat, index) => {
          return <ZoneItem thermostat={thermostat} key={index} />;
        })}
      </Box>
    </Box>
  );
}
