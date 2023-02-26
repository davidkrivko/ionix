import PropTypes from 'prop-types';
import { useState } from 'react';
// material
import { Box, Typography } from '@mui/material';

import ZoneItem from './ZoneItem';
import ZoneEditDialog from './ZoneEditDialog';

// ----------------------------------------------------------------------

ZoneList.propTypes = {
  zone: PropTypes.object.isRequired,
  index: PropTypes.number
};

export default function ZoneList({ zone }) {
  const [name, setName] = useState(zone.name);

  const handleName = (value) => {
    setName(value);
  }

  return (
    <Box
      sx={{
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        rowGap: '5px'
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          columnGap: '2px',
          justifyContent: 'flex-start',
          alignItems: 'center'
        }}
      >
        <Typography variant="body1" fontWeight="bold">
          {name}
        </Typography>
        <ZoneEditDialog zone={zone} onSubmit={handleName} />
      </Box>
      <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10px' }}>
        {zone.thermostats.map((thermostat, index) => {
          return <ZoneItem thermostat={thermostat} key={index} />;
        })}
      </Box>
    </Box>
  );
}
