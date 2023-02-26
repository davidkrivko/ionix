import * as Yup from 'yup';
import { useState } from 'react';
import { useFormik, Form, FormikProvider } from 'formik';
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
  TextField
} from '@mui/material';
import { LoadingButton } from '@mui/lab';

import { MIconButton } from '../../@material-extend';
import { Icon } from '@iconify/react';
import closeFill from '@iconify/icons-eva/close-fill';
import editFill from '@iconify/icons-eva/edit-fill';
import { useSnackbar } from 'notistack';

// hooks
import useIsMountedRef from '../../../hooks/useIsMountedRef';

// utils
import axios from '../../../utils/axios';
import { getCsrfToken } from '../../../utils/thermostats';
// ----------------------------------------------------------------------

const DialogStyle = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2)
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1)
  }
}));
// ----------------------------------------------------------------------

ZoneEditDialog.propTypes = {
  zone: PropTypes.object.isRequired,
  onSubmit: PropTypes.func
};

export default function ZoneEditDialog({ zone, onSubmit }) {
  const isMountedRef = useIsMountedRef();
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const [open, setOpen] = useState(false);

  const ZoneSchema = Yup.object().shape({
    name: Yup.string().min(2, 'Too Short!').max(50, 'Too Long!').required('Name required')
  });

  const formik = useFormik({
    initialValues: {
      name: zone.name || ''
    },
    validationSchema: ZoneSchema,
    onSubmit: async (values, { setErrors, setSubmitting }) => {
      console.log('values:', values);
      const endPoint = `/api/properties/zone/changename/`;
      const csrfToken = getCsrfToken();
      await axios
        .post(
          endPoint,
          { id: zone.id, name: values.name },
          { headers: { 'X-CSRFToken': csrfToken } }
        )
        .then((response) => {
          console.log(response);
          if (response.status === 200) {
            enqueueSnackbar('Zonename was successfully updated.', {
              variant: 'success',
              action: (key) => (
                <MIconButton size="small" onClick={() => closeSnackbar(key)}>
                  <Icon icon={closeFill} />
                </MIconButton>
              )
            });
            onSubmit(values.name);
            setOpen(false);
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

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ maxWidth: '100%' }}>
      <IconButton
        aria-label="edit"
        size="small"
        onClick={handleClickOpen}
        sx={{ color: 'rgb(43, 33, 54)' }}
      >
        <Icon icon={editFill}></Icon>
      </IconButton>
      <DialogStyle onClose={handleClose} aria-labelledby="customized-dialog-title" open={open}>
        <DialogTitle sx={{ m: 0, p: 2 }}>
          <Typography sx={{ fontSize: '18px', fontWeight: '700' }}>Update Zone Name</Typography>
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
        <DialogContent dividers sx={{ width: '350px' }}>
          <FormikProvider value={formik}>
            <Form autoComplete="off" noValidate onSubmit={handleSubmit}>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-start',
                  columnGap: '10px'
                }}
              >
                <Typography variant="span" sx={{ fontSize: '14px' }}>
                  Name:
                </Typography>
                <TextField
                  fullWidth
                  size="small"
                  {...getFieldProps('name')}
                  error={Boolean(touched.name && errors.name)}
                  helperText={touched.name && errors.name}
                  sx={{ flexGrow: 1 }}
                />
              </Box>
              <Box
                style={{
                  marginTop: '10px',
                  display: 'flex',
                  justifyContent: 'flex-end',
                  columnGap: '10px'
                }}
              >
                <LoadingButton variant="contained" size="small" type="submit" loading={isSubmitting}>
                  update
                </LoadingButton>
                <Button variant="outlined" size="small" onClick={handleClose}>
                  Close
                </Button>
              </Box>
            </Form>
          </FormikProvider>
        </DialogContent>
      </DialogStyle>
    </Box>
  );
}
