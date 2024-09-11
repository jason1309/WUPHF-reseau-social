function calculerTempsDepuis(horodatage) {
  var now = new Date();
  var datePublication = new Date(horodatage);
  var diffMs = Math.abs(now - datePublication);
  var diffSecondes = Math.floor(diffMs / 1000);
  var diffMinutes = Math.floor(diffSecondes / 60);
  var diffHeures = Math.floor(diffMinutes / 60);
  var diffJours = Math.floor(diffHeures / 24);
  var diffSemaines = Math.floor(diffJours / 7);

  if (diffSemaines >= 1) {
    return `${diffSemaines} sem - `;
  } else if (diffJours >= 1) {
    return `${diffJours} j - `;
  } else if (diffHeures >= 1) {
    return `${diffHeures} h - `;
  } else if (diffMinutes >= 1) {
    return `${diffMinutes} min - `;
  } else {
    return `à l'instant - `;
  }
}

function boutonModifierProfil() {
  var form = document.getElementById("modification-profil");
  if (form.style.display === "none" || form.style.display === "") {
    form.style.display = "flex";
  } else {
    form.style.display = "none";
  }

}

function convertirDateAJour(dateStr) {
  let days = 0;
  if (dateStr.includes('semaine')) {
    const weeks = parseInt(dateStr.match(/(\d+)/)[0]);
    days = weeks * 7;
  } else if (dateStr.includes('jour')) {
    days = parseInt(dateStr.match(/(\d+)/)[0]);
  } else if (dateStr.includes('heure')) {
    days = parseFloat(dateStr.match(/(\d+)/)[0]) / 24;
  } else if (dateStr.includes('minute')) {
    days = parseFloat(dateStr.match(/(\d+)/)[0]) / (24 * 60);
  } else if (dateStr.includes('seconde')) {
    days = parseFloat(dateStr.match(/(\d+)/)[0]) / (24 * 60 * 60);
  }
  return days;
}
