var simplemaps_countrymap_mapdata = {
  main_settings: {
    // Basic map settings
    width: "600",
    background_color: "#ffffff",
    border_color: "#ffffff",
    popups: "detect",
  },
  state_specific: {
    Kerala: {
      name: "Kerala",
      description: "Backwaters, hills, and culture.",
      color: "#FF4500",
      hover_color: "#FF6347",
      url: "state.html?state=Kerala",
    },
    "Tamil Nadu": {
      name: "Tamil Nadu",
      description: "Temples and coastal beauty.",
      color: "#4682B4",
      hover_color: "#87CEEB",
      url: "state.html?state=Tamil Nadu",
    },
    Karnataka: {
      name: "Karnataka",
      description: "Heritage and modern vibes.",
      color: "#9ACD32",
      hover_color: "#ADFF2F",
      url: "state.html?state=Karnataka",
    },
    "Andhra Pradesh": {
      name: "Andhra Pradesh",
      description: "Rich history and cuisine.",
      color: "#D2691E",
      hover_color: "#FFA07A",
      url: "state.html?state=Andhra Pradesh",
    },
  },
  labels: {
    Kerala: { x: 150, y: 350 },
    "Tamil Nadu": { x: 300, y: 300 },
    Karnataka: { x: 400, y: 250 },
    "Andhra Pradesh": { x: 500, y: 200 },
  },
};