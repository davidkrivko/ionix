import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
// material
import { styled } from '@mui/material/styles';
import {
  Grid,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogActions,
  DialogContent,
  Typography,
  IconButton
} from '@mui/material';
import { Icon } from '@iconify/react';
import closeFill from '@iconify/icons-eva/close-fill';

// utils
import axios from '../../../utils/axios';
import { determiteOnlineStatus } from '../../../utils/thermostats';
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

ControllerDialog.propTypes = {
  serial: PropTypes.string.isRequired
};

export default function ControllerDialog({ serial }) {
  const [open, setOpen] = useState(false);
  const [t1, setT1] = useState('');
  const [t2, setT2] = useState('');
  const [onlineStatus, setOnlineStatus] = useState('offline');

  useEffect(() => {
    getControllerData();
  }, []);
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const getControllerData = async () => {
    if (serial) {
      const endPoint = `/api/devices/v2/controller/data/${serial}/`;
      await axios
        .get(endPoint)
        .then((response) => {
          if (response.status === 200) {
            setT1(response.data.tl);
            setT2(response.data.t2);
            setOnlineStatus(determiteOnlineStatus(response.data.timestamp) ? 'online' : 'offline');
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  return (
    <Box sx={{ maxWidth: '100%' }}>
      <Button
        variant="outlined"
        onClick={handleClickOpen}
        sx={{
          paddingX: '1.5rem',
          maxWidth: '100%',
          display: 'block',
          borderColor: '#1f2937',
          color: '#1f2937',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
          textAlign: 'center',
          '&:hover': {
            backgroundColor: '#1f2937',
            borderColor: '#1f2937',
            color: '#fff'
          }
        }}
      >
        {serial || '--'}
      </Button>
      <DialogStyle onClose={handleClose} aria-labelledby="customized-dialog-title" open={open}>
        <DialogTitle sx={{ m: 0, p: 2 }}>
          <Typography sx={{ fontSize: '18px', fontWeight: '700' }}>
            IONIQ Controller Data
          </Typography>
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
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                IONIQ Controller:
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px', fontWeight: '700' }}>
                {serial || '--'}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                T1:
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                {t1 || '--'}&deg;
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                T2:
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                {t2 || '--'}&deg;
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                Status:
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="span" sx={{ fontSize: '14px' }}>
                {onlineStatus || '--'}
              </Typography>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
            Close
          </Button>
        </DialogActions>
      </DialogStyle>
    </Box>
  );
}
