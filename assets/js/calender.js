document.addEventListener('DOMContentLoaded', async ()=>{
  const res   = await fetch('data/events.json');
  const events= await res.json();
  const cal   = new FullCalendar.Calendar(
    document.getElementById('calendar'),
    { initialView:'dayGridMonth', locale:'ja', events }
  );
  cal.render();
});
