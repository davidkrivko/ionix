// material
import { styled } from '@mui/material/styles';
import { Box, Typography } from '@mui/material';

// ----------------------------------------------------------------------

const RootStyle = styled('div')(() => ({
  boxShadow: 'none',
  backdropFilter: 'blur(6px)',
  WebkitBackdropFilter: 'blur(6px)',
  backgroundColor: '#000',
  padding: '16px 24px'
}));

// ----------------------------------------------------------------------

export default function DashboardFooter() {
  return (
    <RootStyle>
      <Box>
        <Typography variant="body2" sx={{ color: '#fff' }}>
          © IONIQBOX 2023 - support@turnonheat.com
        </Typography>
      </Box>
    </RootStyle>
  );
}
