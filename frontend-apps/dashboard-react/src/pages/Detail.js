// material
import { Container, Stack } from '@mui/material';
// components
import Page from '../components/Page';
import { ZoneDetail } from '../components/_main/zone';
//
// ----------------------------------------------------------------------

export default function List() {
  return (
    <Page title="Dashboard: List | IONIC">
      <Container>
        <Stack direction="column" alignItems="center" spacing={2}>
          <ZoneDetail />
        </Stack>
      </Container>
    </Page>
  );
}
