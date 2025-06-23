const BASE_URL = "https://api.reliefweb.int/v1/disasters";

/**
 * Fetch recent disasters (latest 20 worldwide)
 * @returns {Promise<Array>} List of disaster events
 */
export async function fetchRecentDisasters() {
  try {
    // ReliefWeb: GET /disasters?appname=FlashRisk&limit=20&sort[]=date:desc
    const url = `${BASE_URL}?appname=FlashRisk&limit=20&sort[]=date:desc`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch disaster data");
    const data = await res.json();
    // ReliefWeb returns data array
    return data.data || [];
  } catch (err) {
    console.error("Error fetching disasters:", err);
    return [];
  }
}

/**
 * Fetch disaster details by ID
 * @param {string} id - Disaster event ID
 * @returns {Promise<Object|null>} Disaster details or null on error
 */
export async function fetchDisasterById(id) {
  try {
    const url = `${BASE_URL}/${id}?appname=FlashRisk`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch disaster details");
    const data = await res.json();
    // ReliefWeb returns data array with one result
    return data.data && data.data[0] ? data.data[0] : null;
  } catch (err) {
    console.error(`Error fetching disaster ${id}:`, err);
    return null;
  }
}
