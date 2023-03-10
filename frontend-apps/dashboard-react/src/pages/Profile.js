import { useState, useEffect } from 'react';
// material
import { Container, Stack, Card, Box, Button, Typography } from '@mui/material';
import { Icon } from '@iconify/react';
import arrowBackFill from '@iconify/icons-eva/arrow-back-fill';

import { useNavigate } from 'react-router-dom';
// components
import Page from '../components/Page';
import { GeneralProfile, ChangePassword } from '../components/_main/profile';
// utils
import axios from '../utils/axios';
// ----------------------------------------------------------------------

export default function Profile() {
  const navigate = useNavigate();
  const [showPassForm, setShowPassForm] = useState(false);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    getUserData();
  }, []);

  const goBack = () => {
    navigate(-1);
  };

  const getUserData = async () => {
    const endPoint = `/api/users/me/`;
    await axios
      .get(endPoint)
      .then((response) => {
          console.log("response:", response);
        if (response.status === 200) {
          setProfile(response.data);
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
          <Card
            sx={{
              maxWidth: '500px',
              padding: '3rem 2rem',
              display: 'flex',
              flexDirection: 'column',
              rowGap: '1.5rem'
            }}
          >
            <Box
              sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', columnGap: '5px' }}
            >
              <Box
                component={Icon}
                icon={arrowBackFill}
                sx={{ width: 20, height: 20, mr: 0.5, cursor: 'pointer' }}
                onClick={goBack}
              />
              <Typography variant="body1" fontWeight="bold">
                Profile Settings
              </Typography>
            </Box>
            <GeneralProfile profile={profile} />
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-start',
                columnGap: '10px'
              }}
            >
              <Button size="small" onClick={() => setShowPassForm(true)}>
                Update Password
              </Button>
            </Box>
            {showPassForm ? <ChangePassword /> : <></>}
          </Card>
        </Stack>
      </Container>
    </Page>
  );
}
