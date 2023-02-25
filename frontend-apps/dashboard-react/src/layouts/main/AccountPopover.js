import { Icon } from '@iconify/react';
import { useRef, useState } from 'react';
import personFill from '@iconify/icons-eva/person-fill';
import logoutFill from '@iconify/icons-eva/log-out-fill';
import { Link as RouterLink } from 'react-router-dom';
// material
import { Button, Box, MenuItem } from '@mui/material';
// components
import MenuPopover from '../../components/MenuPopover';

// ----------------------------------------------------------------------

const MENU_OPTIONS = [
  {
    label: 'Profile',
    icon: personFill,
    linkTo: '/dashboard/profile'
  },
  {
    label: 'Logout',
    icon: logoutFill,
    linkTo: '#'
  }
];

// ----------------------------------------------------------------------

export default function AccountPopover() {
  const anchorRef = useRef(null);
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Button
        variant="contained"
        size="md"
        ref={anchorRef}
        onClick={handleOpen}
        sx={{
          backgroundColor: '#3d4451',
          textTransform: 'uppercase',
          fontSize: '14px',
          boxShadow: 'none',
          padding: '0.6rem 1rem',
          color: '#fff',
          '&:hover': {
            backgroundColor: '#303640',
            boxShadow: 'none'
          }
        }}
      >
        Account
      </Button>

      <MenuPopover
        open={open}
        onClose={handleClose}
        anchorEl={anchorRef.current}
        sx={{ width: 220, paddingTop: '10px', paddingBottom: '10px' }}
      >
        {MENU_OPTIONS.map((option) => (
          <MenuItem
            key={option.label}
            to={option.linkTo}
            component={RouterLink}
            onClick={handleClose}
            sx={{ typography: 'body2', py: 1, px: 2.5 }}
          >
            <Box
              component={Icon}
              icon={option.icon}
              sx={{
                mr: 2,
                width: 24,
                height: 24
              }}
            />

            {option.label}
          </MenuItem>
        ))}
      </MenuPopover>
    </>
  );
}
