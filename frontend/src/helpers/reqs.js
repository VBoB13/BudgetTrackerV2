import axios from "axios";

export function isResponseOK(response) {
  if (response.status >= 200 && response.status <= 299) {
    return new Promise((resolve, reject)=> {
      if (response.data) return resolve(response.data);
      return reject(response);
    });

  } else if (response.status >= 400 && response.status <= 499) {
    if (response.data) return response.data;
    return response;
  } else {
    throw new Error("Response ERROR!");
  }
}

export class RequestHandler {
  constructor(url, method = "GET", contentType = "application/json") {
    this.url = url;
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
  sendRequest(default_response = {}) {
    return new Promise((resolve, reject) => {
      axios(this.reqConf)
        .then((response) => {
          if (response.status >= 200 && response.status <= 399) {
            resolve(response.data);
          } else {
            if (Object.getOwnPropertyNames(default_response).length === 0)
              reject(response.statusText);
            reject(default_response);
          }
        })
        .catch((error) => {
          console.log(error);
          reject(default_response);
        });
    });
  }
}
