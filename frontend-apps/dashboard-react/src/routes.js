import { Navigate, useRoutes } from 'react-router-dom';
// layouts
import MainLayout from './layouts/main';
//
import List from './pages/List';
import Detail from './pages/Detail';
import Profile from './pages/Profile';

// ----------------------------------------------------------------------

export default function Router() {
  return useRoutes([
    {
      path: '/',
      element: <MainLayout />,
      children: [
        { path: 'app', element: <List /> },
        { path: 'detail', element: <Detail /> },
        { path: 'profile', element: <Profile /> },
      ]
    },
  ]);
}
