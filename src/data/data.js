/* ============================================================================
 * data.js — THE ONLY file you should need to edit to change site content.
 *
 * Everything the room shows (About panel, project shelf, contact card) is
 * read from this file. Add/remove a project by editing the `projects` array
 * and dropping its thumbnail in public/assets/projects/ — no scene or
 * animation code needs to change. `shelfSlot` must match one of the model
 * keys baked into public/assets/room/room-layout.json ("store", "phone",
 * "robot", "tower", "dashboard", "apps").
 * ========================================================================== */

export const portfolioData = {
  profile: {
    firstName: "Mahdi",
    lastName: "Montazeri",
    fullName: "Mahdi Montazeri Najafabadi",
    role: "Software Developer",
    roleLong: "Aspiring Computer Science / Artificial Intelligence Undergraduate",
    tagline:
      "I build web platforms, Android apps and robot software. Currently heading into a Computer Science and AI degree.",
    status: "Open to internships",
    location: "Isfahan, Iran",
    photo: "assets/profile.jpg",
    bio:
      "High school graduate in Network & Software with a diploma GPA of 18.57/20. " +
      "Interested in Computer Science and AI, with practical experience building " +
      "Android applications, web platforms, and software for robotics and " +
      "environmental-monitoring projects.",
    education: {
      degree: "High School Diploma — Network & Software",
      school: "Abuzar Technical & Vocational School, Isfahan, Iran",
      years: "2023–2026",
      gpa: "18.57 / 20",
    },
    languages: [
      { name: "Persian", level: "Native" },
      { name: "English", level: "B1+ (preparing for an official certificate)" },
    ],
    interests: [
      "Computer Science",
      "Artificial Intelligence",
      "Machine Learning",
      "Robotics & Embedded Systems",
    ],
  },

  /* ---- PROJECTS — rendered on the shelf, one object per entry ----------
     shelfSlot: 0-5, maps to the baked models in room-layout.json
     ("proj-store", "proj-phone", "proj-robot", "proj-tower",
      "proj-dashboard", "proj-apps"), in that left-to-right order.
     links: leave a field "" to hide its button — never a broken link. */
  projects: [
    {
      id: "hamrahmadrese",
      title: "HamrahMadrese",
      category: "Web Platform",
      year: 2026,
      status: "Live product",
      shelfSlot: 0,
      description:
        "Educational marketplace built with Django, Python and MySQL. " +
        "Account authentication, phone OTP verification, educational " +
        "product/content management, Zarinpal payment integration, digital " +
        "purchases and downloads, and production deployment & maintenance.",
      technologies: ["Python", "Django", "MySQL", "Zarinpal API"],
      links: { github: "https://github.com/montatech", demo: "" },
    },
    {
      id: "focus-leaf",
      title: "Focus Leaf",
      category: "Android App",
      year: 2026,
      status: "Independent project",
      shelfSlot: 1,
      description:
        "Android productivity app to help users manage focus goals and " +
        "reduce distractions: timed focus sessions, a Deep Focus mode with " +
        "a selectable allow-list of apps, short breaks, an emergency " +
        "unlock, and a dark UI.",
      technologies: ["Kotlin", "Android", "Jetpack Compose"],
      links: { github: "https://github.com/montatech", demo: "" },
    },
    {
      id: "first-global",
      title: "FIRST Global Challenge — Team Iran",
      category: "Robotics",
      year: "2025–2026",
      status: "Team project",
      shelfSlot: 2,
      description:
        "Software for Team Iran's competition robots across two seasons: " +
        "Java / OnBot Java, motor and servo control, holonomic drive, " +
        "IMU-based movement, AprilTag-related functions, and autonomous " +
        "robot behaviour.",
      technologies: ["Java", "OnBot Java", "Robotics"],
      links: { github: "https://github.com/montatech", demo: "" },
    },
    {
      id: "pyroguard",
      title: "PyroGuard",
      category: "Robotics / IoT",
      year: 2025,
      status: "Team project",
      shelfSlot: 3,
      description:
        "Wildfire sensor / IoT project: sensor-node communication and " +
        "embedded software for an environmental-monitoring concept, using " +
        "Arduino/C++ and sensor data transmission.",
      technologies: ["Arduino", "C++", "ESP32"],
      links: { github: "https://github.com/montatech", demo: "" },
    },
    {
      id: "simorgh",
      title: "Simorgh",
      category: "Web Platform",
      year: 2026,
      status: "Team project",
      shelfSlot: 4,
      description:
        "Wildfire-risk monitoring platform: web-platform components " +
        "including a sensor dashboard and wildfire-risk visualization, " +
        "combining field sensor readings with vegetation information for " +
        "risk awareness.",
      technologies: ["Dashboard", "Data visualisation"],
      links: { github: "https://github.com/montatech", demo: "" },
    },
    {
      id: "android-apps",
      title: "Flower Shop, Currency Tracker & Notes",
      category: "Android Apps",
      year: "2024–2025",
      status: "Personal projects",
      shelfSlot: 5,
      description:
        "Three small Android apps built while practising lists, " +
        "navigation, local storage and live data: a flower/plant shop, a " +
        "currency tracker, and a notes app.",
      technologies: ["Kotlin", "Jetpack Compose", "SQLite"],
      links: { github: "https://github.com/montatech", demo: "" },
    },
  ],

  /* ---- EVE — draft project, shown only if you fill it in ---------------
     Leave title empty to keep it hidden from the shelf. */
  draftProject: {
    id: "eve",
    title: "",
    category: "Draft",
    description: "",
    technologies: [],
    links: { github: "", demo: "" },
  },

  skills: [
    {
      id: "web",
      title: "Web platforms",
      description:
        "Full stacks with accounts, payments and admin screens, then " +
        "deployed and kept running. HamrahMadrese is live with OTP login " +
        "and Zarinpal checkout.",
      tools: ["Python", "Django", "Spring Boot", "MySQL", "HTML / CSS / JS"],
    },
    {
      id: "android",
      title: "Android apps",
      description:
        "Native apps in Kotlin with Jetpack Compose. Focus Leaf, my " +
        "newest, helps people stay off their phones when it matters.",
      tools: ["Kotlin", "Jetpack Compose", "Android Studio", "SQLite"],
    },
    {
      id: "robotics",
      title: "Robotics & embedded",
      description:
        "Motor and servo control, IMU-based movement, AprilTag functions " +
        "and autonomous routines for competition robots, plus sensor " +
        "nodes on Arduino and ESP32.",
      tools: ["Java", "OnBot Java", "C++", "Arduino", "ESP32", "PlatformIO"],
    },
    {
      id: "ai",
      title: "AI & machine learning",
      description:
        "Where I'm heading next: learning data science and machine " +
        "learning in Python, aiming for a Computer Science or AI degree.",
      tools: ["Python", "Data science", "Machine learning"],
    },
  ],

  otherTools: [
    "MySQL", "SQLite", "Git & GitHub", "Postman", "Android Studio",
    "IntelliJ IDEA", "VS Code", "Arduino", "ESP32", "PlatformIO",
  ],

  achievements: {
    statNumber: 3,
    statLabel: "international medals & awards",
    medals: [
      {
        title: "Silver Medal",
        event: "International Tournament of Engineering (ITE), London",
        year: "2023",
        description: "Team award for our engineering project, competing against teams from around the world.",
      },
      {
        title: "Silver Award — New Tech Experience",
        event: "FIRST Global Challenge, Team Iran",
        year: "2025",
        description: "Recognised for the robot's technical design and the software behind its autonomous behaviour.",
      },
      {
        title: "Silver Award — Courageous Achievement",
        event: "FIRST Global Challenge, Team Iran",
        year: "2025",
        description: "Awarded to the team for persistence and problem-solving under competition pressure.",
      },
    ],
    more: [
      "Volunteer Instructor — taught introductory technical concepts to young children during a summer program",
      "Installed and maintained classroom projectors (data show units) and computers at school",
      "Summer R&D internship, Snowa Tech",
      "First Aid training course, Red Crescent Society",
      "2nd place, school video game competition",
      "Completed training programs in Karate, Table Tennis, Volleyball, Chess, and Bodybuilding",
      "Plays the Santur (traditional Persian hammered dulcimer)",
    ],
  },

  contact: {
    email: "mahdimont67@gmail.com",
    phone: "+989905644366",
    github: "https://github.com/montatech",
    linkedin: "",
    resume: "assets/files/Mahdi_Montazeri_CV.pdf",
  },
};

