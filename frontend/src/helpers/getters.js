import { RequestHandler } from "./reqs";

export async function get_all_categories(){
    const reqObj = new RequestHandler("http://0.0.0.0:8000/categories/get_all");
    return await reqObj.sendRequest([
        {
            "id": 1,
            "name": "Food",
            "color": "Green"
        },
        {
            "id": 2,
            "name": "Rent & Utilities",
            "color": "Gray"
        },
        {
            "id": 3,
            "name": "Medical",
            "color": "Pink"
        },
        {
            "id": 4,
            "name": "Leisure",
            "color": "Blue"
        },
        {
            "id": 5,
            "name": "Travel",
            "color": "LightBlue"
        },
        {
            "id": 6,
            "name": "Others",
            "color": "LightGray"
        }
    ]).then(data => data.catetogies);
}