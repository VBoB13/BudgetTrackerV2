import axios from "axios";

export class RequestHandler {
  constructor(url, method = "GET", contentType = "application/json") {
    this.url = "http://" + import.meta.env.VITE_BT_HOST + url;
    this.method = method;
    this.contentType = contentType;
    this.reqConf = {
      method: this.method,
      url: this.url,
      headers: {
        "Content-Type": this.contentType,
        "Access-Control-Allow-Origin": "127.0.0.1:8000",
      },
      credentials: "same-origin",
      data: {},
    };
  }
  sendRequest() {
    return new Promise((resolve, reject) => {
      axios(this.reqConf)
        .then((response) => {
          if (response.status >= 200 && response.status <= 399) {
            resolve(response.data);
          } else {
            reject(response.statusText);
          }
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  }
}
