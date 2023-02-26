import React, { useState, useEffect } from 'react';
// material
import { Container, Stack } from '@mui/material';
// components
import Page from '../components/Page';

// utils
import axios from '../utils/axios';

import { ZoneList } from '../components/_main/zone';
// ----------------------------------------------------------------------

export default function List() {
  const [zones, setZones] = useState([]);

  useEffect(() => {
    getAllZones();
  }, []);

  const getAllZones = async () => {
    await axios
      .get('/api/devices/v2/thermostats/')
      .then((response) => {
        if (response.status === 200) {
          let result = [];
          const data = response.data;
          data.map((item) => {
            const { id: zoneId, name: zoneName } = item.zone;
            delete item.zone;
            const exist = result.find((el) => el.id === zoneId);
            if (exist) {
              result = result.map((el) => {
                let temp = Object.assign({}, el);
                if (temp.id === zoneId) {
                  temp.thermostats.push(item);
                }
                return temp;
              });
            } else {
              const temp = {
                id: zoneId,
                name: zoneName,
                thermostats: [item]
              };
              result.push(temp);
            }
          });
          setZones(result);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <Page title="Dashboard: List | IONIC">
      <Container>
        <Stack direction="column" alignItems="center" spacing={2}>
          {zones.map((zone) => (
            <ZoneList key={zone.id} zone={zone} />
          ))}
        </Stack>
      </Container>
    </Page>
  );
}
