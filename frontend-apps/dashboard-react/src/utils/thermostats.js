const csrfTokenExists = () => {
  if (document.cookie.split(';').some((item) => item.trim().startsWith('csrftoken='))) {
    return true;
  } else {
    return false;
  }
}

export const getCsrfToken = () => {
  if (csrfTokenExists()) {
    return document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrftoken='))
      .split('=')[1];
  }
};

export const formatTimeAgo = (date) => {
  if (!date) return '--';
  return timeAgo.format(date);
}

export const determiteOnlineStatus = (timestamp) => {
  if (!timestamp) return false;
  const diff = Math.abs(new Date() - new Date(timestamp));
  const delta_min = Math.round(diff / 1000 / 60);

  if (delta_min < 3) {
    return true;
  }
  return false;
};
