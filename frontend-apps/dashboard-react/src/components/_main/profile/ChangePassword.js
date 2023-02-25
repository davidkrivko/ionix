import * as Yup from 'yup';
import { useState } from 'react';
import { useFormik, Form, FormikProvider } from 'formik';

// material
import { styled } from '@mui/material/styles';
import { Grid, Typography, TextField, IconButton, InputAdornment } from '@mui/material';
import { LoadingButton } from '@mui/lab';

import { MIconButton } from '../../@material-extend';
import { Icon } from '@iconify/react';
import eyeFill from '@iconify/icons-eva/eye-fill';
import eyeOffFill from '@iconify/icons-eva/eye-off-fill';
import closeFill from '@iconify/icons-eva/close-fill';
import { useSnackbar } from 'notistack';

// hooks
import useIsMountedRef from '../../../hooks/useIsMountedRef';

// utils
import axios from '../../../utils/axios';
import { getCsrfToken } from '../../../utils/thermostats';
import { passwordError } from '../../../utils/helpError';
// ----------------------------------------------------------------------

const RootStyle = styled('div')({
  width: '100%'
});

// ----------------------------------------------------------------------

export default function ChangePassword() {
  const isMountedRef = useIsMountedRef();
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showNewConfirmPassword, setShowNewConfirmPassword] = useState(false);

  const ChangePasswordSchema = Yup.object().shape({
    oldPassword: Yup.string().required('Old password is required'),
    newPassword: Yup.string().required('New password is required'),
    newPasswordConfirm: Yup.string()
      .required('New password confirm is required')
      .oneOf([Yup.ref('newPassword'), null], 'Passwords does not match')
  });

  const formik = useFormik({
    initialValues: {
      oldPassword: '',
      newPassword: '',
      newPasswordConfirm: ''
    },
    validationSchema: ChangePasswordSchema,
    onSubmit: async (values, { setErrors, setSubmitting }) => {
      const endPoint = `/api/users/password/update/`;
      const csrfToken = getCsrfToken();
      const data = {
        old_password: values.oldPassword,
        new_password: values.newPassword
      };
      await axios
        .post(endPoint, data, { headers: { 'X-CSRFToken': csrfToken } })
        .then((response) => {
          if (response.status === 200) {
            enqueueSnackbar('Password successfully updated.', {
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

  const handleShowOldPassword = () => {
    setShowOldPassword((show) => !show);
  };

  const handleShowNewPassword = () => {
    setShowNewPassword((show) => !show);
  };

  const handleShowNewConfirmPassword = () => {
    setShowNewConfirmPassword((show) => !show);
  };

  return (
    <RootStyle>
      <FormikProvider value={formik}>
        <Form autoComplete="off" noValidate onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                Current Password:
              </Typography>
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <TextField
                fullWidth
                size="small"
                autoComplete="current-password"
                type={showOldPassword ? 'text' : 'password'}
                {...getFieldProps('oldPassword')}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={handleShowOldPassword} edge="end">
                        <Icon icon={showOldPassword ? eyeFill : eyeOffFill} />
                      </IconButton>
                    </InputAdornment>
                  )
                }}
                error={
                  Boolean(touched.oldPassword && errors.oldPassword) ||
                  passwordError(errors.afterSubmit).error
                }
                helperText={
                  (touched.oldPassword && errors.oldPassword) ||
                  passwordError(errors.afterSubmit).helperText
                }
              />
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                New Password:
              </Typography>
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <TextField
                fullWidth
                size="small"
                autoComplete="new-password"
                type={showNewPassword ? 'text' : 'password'}
                {...getFieldProps('newPassword')}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={handleShowNewPassword} edge="end">
                        <Icon icon={showNewPassword ? eyeFill : eyeOffFill} />
                      </IconButton>
                    </InputAdornment>
                  )
                }}
                error={Boolean(touched.newPassword && errors.newPassword)}
                helperText={touched.newPassword && errors.newPassword}
              />
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                New Password Confirm:
              </Typography>
            </Grid>
            <Grid item xs={6} md={6} display="flex" alignItems="center">
              <TextField
                fullWidth
                size="small"
                autoComplete="new-password-confirm"
                type={showNewConfirmPassword ? 'text' : 'password'}
                {...getFieldProps('newPasswordConfirm')}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={handleShowNewConfirmPassword} edge="end">
                        <Icon icon={showNewConfirmPassword ? eyeFill : eyeOffFill} />
                      </IconButton>
                    </InputAdornment>
                  )
                }}
                error={Boolean(touched.newPasswordConfirm && errors.newPasswordConfirm)}
                helperText={touched.newPasswordConfirm && errors.newPasswordConfirm}
              />
            </Grid>
            <Grid item xs={12} md={12} display="flex" alignItems="center">
              <LoadingButton variant="contained" size="small" type="submit" color="primary" loading={isSubmitting}>
                Update
              </LoadingButton>
            </Grid>
          </Grid>
        </Form>
      </FormikProvider>
    </RootStyle>
  );
}
