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