const NOW = new Date();
const MONTH =
  NOW.getMonth() + 1 < 10 ? `0${NOW.getMonth() + 1}` : `${NOW.getMonth() + 1}`;
export const TODAY = `${NOW.getFullYear()}-${MONTH}-${
  NOW.getDate() < 10 ? "0" + NOW.getDate() : NOW.getDate()
}`;

export const CATEGORY_COLORS = {
  "Food": "#008000",
  "Life": "#0000b3",
  "Rent & Utilities": "#808080",
  "Medical": "#ffc0cb",
  "Leisure": "#1a1aff",
  "Travel": "#ff0000",
  "Kitties": "#58a8f8",
  "Transportation": "#ffff80",
  "Debt": "#800000",
  "Others": "#bfbfbf"
};