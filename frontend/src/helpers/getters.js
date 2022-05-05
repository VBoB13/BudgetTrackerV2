import { RequestHandler } from "./reqs";

export function get_all_categories(){
    const reqObj = new RequestHandler("http://0.0.0.0:8000/categories/get_all");
    return reqObj.sendRequest(["Food", "Rent & Utilities", "Leisure", "Travel", "Others"]).then(data => data).catch(default_data => {
        return default_data;
    });
}