import axios from "axios";

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


export async function fetchIoniqOnlineStatus(controller_sn) {

  try {
      const endpoint = '/api/devices/controller/status/';
      const csrfcookie = getCsrfCookieValue();
      const data = {
      "sn": controller_sn
      }
      const response = await axios({
          url: endpoint,
          method: "post",
          data: data,
          headers: {
          'X-CSRFToken': csrfcookie
          }

      });
      if(response.status === 200) {
          const res = response.data.data;
          console.log("controller status response", response.data)
          return res;
          }
  } catch(error) {
        console.log(error)
}
};
