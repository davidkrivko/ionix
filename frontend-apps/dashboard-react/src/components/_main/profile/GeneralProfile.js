import * as Yup from 'yup';
import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { useFormik, Form, FormikProvider } from 'formik';

// material
import { styled } from '@mui/material/styles';
import { Grid, Typography, TextField } from '@mui/material';
import { LoadingButton } from '@mui/lab';

import { MIconButton } from '../../@material-extend';
import { Icon } from '@iconify/react';
import closeFill from '@iconify/icons-eva/close-fill';
import { useSnackbar } from 'notistack';

// hooks
import useIsMountedRef from '../../../hooks/useIsMountedRef';
// utils
import axios from '../../../utils/axios';
import { getCsrfToken } from '../../../utils/thermostats';

// ----------------------------------------------------------------------
const RootStyle = styled('div')({
  width: '100%'
});
// ----------------------------------------------------------------------
GeneralProfile.propTypes = {
  profile: PropTypes.object
};

export default function GeneralProfile({ profile }) {
  console.log("profile:", profile);
  const isMountedRef = useIsMountedRef();
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const ProfileSchema = Yup.object().shape({
    first_name: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Name required'),
    email: Yup.string().email('Email must be a valid email address').required('Email is required')
  });

  const formik = useFormik({
    initialValues: {
      first_name: profile ? profile.first_name : '',
      email: profile ? profile.email : ''
    },
    validationSchema: ProfileSchema,
    onSubmit: async (values, { setErrors, setSubmitting }) => {
      const endPoint = `/api/users/owner/profile/update/`;
      const csrfToken = getCsrfToken();
      await axios
        .post(endPoint, values, { headers: { 'X-CSRFToken': csrfToken } })
        .then((response) => {
          if (response.status === 200) {
            enqueueSnackbar('Profile successfully updated.', {
              variant: 'success',
              action: (key) => (
                <MIconButton size="small" onClick={() => closeSnackbar(key)}>
                  <Icon icon={closeFill} />
                </MIconButton>
              )
            });
            if (isMountedRef.current) {
              setSubmitting(false);
            }
          }
        })
        .catch((error) => {
          if (isMountedRef.current) {
            setErrors({ afterSubmit: error.code });
            setSubmitting(false);
          }
        });
    }
  });

  const { errors, touched, handleSubmit, isSubmitting, getFieldProps } = formik;

  return (
    <RootStyle>
      <FormikProvider value={formik}>
        <Form autoComplete="off" noValidate onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                Name:
              </Typography>
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <TextField
                fullWidth
                size="small"
                {...getFieldProps('first_name')}
                error={Boolean(touched.first_name && errors.first_name)}
                helperText={touched.first_name && errors.first_name}
              />
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                Email:
              </Typography>
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <TextField
                fullWidth
                size="small"
                autoComplete="email"
                type="email"
                {...getFieldProps('email')}
                error={Boolean(touched.email && errors.email)}
                helperText={touched.email && errors.email}
              />
            </Grid>
            <Grid item xs={12} md={12} display="flex" alignItems="center">
              <LoadingButton variant="outlined" size="small" type="submit" loading={isSubmitting}>
                Save
              </LoadingButton>
            </Grid>
          </Grid>
        </Form>
      </FormikProvider>
    </RootStyle>
  );
}
