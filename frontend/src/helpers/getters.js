import { RequestHandler } from "./reqs";

export async function get_all_categories(){
    const reqObj = new RequestHandler("http://0.0.0.0:8000/categories/get_all");
    return await reqObj.sendRequest(["Food", "Rent & Utilities", "Leisure", "Travel", "Others"]);
}