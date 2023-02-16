import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";

TimeAgo.addDefaultLocale(en);
const timeAgo = new TimeAgo("en-US");



function checkACookieExists() {
  if (document.cookie.split(';').some((item) => item.trim().startsWith('csrftoken='))) {
    return true;
  } else {
    return false;
  }
}

export const getCsrfCookieValue = () => {
  if (checkACookieExists()) {
    return document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      .split('=')[1];
  }
}

export function formatTimeAgo(date) {
  if (!date) return '--';
  return timeAgo.format(date);
}

export function determiteOnlineStatus(timestamp) {
  // console.log("timestamp", timestamp)
  if (!timestamp) return false;
  const diff = Math.abs(new Date() - new Date(timestamp));
  // console.log("diff", diff)
  const delta_min = Math.round(diff / 1000 / 60);

  if (delta_min < 3) {
    return true;
  }
  return false;
}