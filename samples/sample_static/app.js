// The menu and opening hours. Change them here; the page draws itself from these lists.
const MENU = [
    { name: "Espresso", note: "Single origin, changes weekly", price: "$3.00", type: "coffee" },
    { name: "Flat white", note: "Double shot, steamed milk", price: "$4.50", type: "coffee" },
    { name: "House filter", note: "Brewed by the cup", price: "$4.00", type: "coffee" },
    { name: "Sencha", note: "Loose-leaf green tea", price: "$3.80", type: "tea" },
    { name: "Masala chai", note: "Spiced, with oat milk", price: "$4.80", type: "tea" },
    { name: "Butter croissant", note: "Baked this morning", price: "$3.50", type: "bakery" },
    { name: "Cardamom bun", note: "Our most asked-for", price: "$4.20", type: "bakery" },
];

// 0 is Sunday. Times are 24-hour, in the visitor's own time zone.
const HOURS = [
    { day: "Sunday", open: "08:00", close: "15:00" },
    { day: "Monday", open: "07:00", close: "17:00" },
    { day: "Tuesday", open: "07:00", close: "17:00" },
    { day: "Wednesday", open: "07:00", close: "17:00" },
    { day: "Thursday", open: "07:00", close: "17:00" },
    { day: "Friday", open: "07:00", close: "18:00" },
    { day: "Saturday", open: "08:00", close: "18:00" },
];

function showMenu(type) {
    const list = document.getElementById("menuList");
    list.replaceChildren(...MENU.filter((item) => type === "all" || item.type === type).map((item) => {
        const row = document.createElement("li");
        const name = document.createElement("span");
        name.textContent = item.name;
        const note = document.createElement("span");
        note.className = "note";
        note.textContent = item.note;
        name.append(note);
        const price = document.createElement("span");
        price.className = "price";
        price.textContent = item.price;
        row.append(name, price);
        return row;
    }));
}

function minutes(time) {
    const [hours, mins] = time.split(":").map(Number);
    return hours * 60 + mins;
}

function showHours() {
    const now = new Date();
    const today = HOURS[now.getDay()];
    const current = now.getHours() * 60 + now.getMinutes();
    const open = current >= minutes(today.open) && current < minutes(today.close);

    const badge = document.getElementById("openBadge");
    badge.textContent = open ? `Open now, until ${today.close}` : `Closed now. Today ${today.open} to ${today.close}`;
    badge.classList.toggle("is-open", open);

    const list = document.getElementById("hoursList");
    HOURS.forEach((entry, index) => {
        const day = document.createElement("dt");
        day.textContent = entry.day;
        const time = document.createElement("dd");
        time.textContent = `${entry.open} to ${entry.close}`;
        if (index === now.getDay()) {
            day.classList.add("today");
            time.classList.add("today");
        }
        list.append(day, time);
    });
}

document.querySelectorAll(".filter").forEach((button) => {
    button.addEventListener("click", () => {
        document.querySelectorAll(".filter").forEach((other) => other.classList.toggle("is-active", other === button));
        showMenu(button.dataset.filter);
    });
});

showMenu("all");
showHours();
