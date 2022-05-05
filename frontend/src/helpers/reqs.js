import axios from "axios";

export function isResponseOK(response) {
  console.log(response);
  if (response.status >= 200 && response.status <= 299) {
    if (response.data) return response.data;
    return response;
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
      },
      credentials: "same-origin",
      data: {}
    };
  }
  async sendRequest() {
    const response = await axios(this.reqConf);
    let data = isResponseOK(response);
    return data;
  }
}
