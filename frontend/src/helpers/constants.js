const NOW = new Date();
const MONTH =
  NOW.getMonth() + 1 < 10 ? `0${NOW.getMonth() + 1}` : `${NOW.getMonth() + 1}`;
export const TODAY = `${NOW.getFullYear()}-${MONTH}-${
  NOW.getDate() < 10 ? "0" + NOW.getDate() : NOW.getDate()
}`;