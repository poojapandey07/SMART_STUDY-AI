/* ==========================================================================
   SMARTSTUDY AI - REALISTIC COLLEGE STUDENT DATASET
   ========================================================================== */

const DEFAULT_DATA = {
  user: {
    name: "Pooja Sharma",
    email: "pooja@smartstudy.ai",
    major: "Computer Science & Engineering",
    university: "Government Engineering College",
    studyGoalHours: 3.5,
    streak: 5
  },

  tasks: [
    {
      id: 1,
      title: "Revise array operations and two-pointer technique",
      subject: "Data Structures",
      subjectKey: "ds",
      priority: "high",
      deadline: "Today, 5:00 PM",
      duration: "45 min",
      description: "Practice two-sum and sliding window problems",
      completed: true
    },
    {
      id: 2,
      title: "Practice 10 Python list comprehension questions",
      subject: "Python",
      subjectKey: "py",
      priority: "high",
      deadline: "Today, 7:30 PM",
      duration: "60 min",
      description: "Solve dictionary and list comprehension exercises",
      completed: false
    },
    {
      id: 3,
      title: "Read DBMS normalization notes (1NF to 3NF)",
      subject: "Database Management",
      subjectKey: "dbms",
      priority: "med",
      deadline: "Tomorrow, 2:00 PM",
      duration: "50 min",
      description: "Review functional dependencies and lossless join decomposition",
      completed: false
    },
    {
      id: 4,
      title: "Prepare OS process scheduling (Round Robin & SJF)",
      subject: "Operating Systems",
      subjectKey: "os",
      priority: "med",
      deadline: "Oct 6, 11:00 AM",
      duration: "60 min",
      description: "Calculate average waiting time and turnaround time numericals",
      completed: false
    },
    {
      id: 5,
      title: "Review neural network backpropagation steps",
      subject: "Artificial Intelligence",
      subjectKey: "ai",
      priority: "low",
      deadline: "Oct 7, 4:00 PM",
      duration: "40 min",
      description: "Derive chain rule gradients for weights and biases",
      completed: true
    }
  ],

  scheduleToday: [
    { id: 1, time: "09:00 AM - 10:00 AM", title: "Array Operations & Two-Pointer Workshop", subject: "Data Structures", status: "completed" },
    { id: 2, time: "11:00 AM - 12:00 PM", title: "List Comprehensions & Generator Functions", subject: "Python", status: "completed" },
    { id: 3, time: "02:00 PM - 03:15 PM", title: "Normalization & BCNF Practice", subject: "Database Management", status: "in-progress" },
    { id: 4, time: "04:30 PM - 05:30 PM", title: "CPU Scheduling Algorithms & Gantt Charts", subject: "Operating Systems", status: "upcoming" },
    { id: 5, time: "07:00 PM - 07:45 PM", title: "AI Tutor Quick Revision & 5-Question Quiz", subject: "Artificial Intelligence", status: "upcoming" }
  ],

  weeklyHours: [
    { day: "Mon", hours: 2.0, label: "2.0h" },
    { day: "Tue", hours: 3.5, label: "3.5h" },
    { day: "Wed", hours: 2.5, label: "2.5h" },
    { day: "Thu", hours: 4.0, label: "4.0h" },
    { day: "Fri", hours: 3.0, label: "3.0h" },
    { day: "Sat", hours: 3.5, label: "3.5h" },
    { day: "Sun", hours: 1.75, label: "1.75h (Today)" }
  ],

  subjectProgress: [
    { subject: "Data Structures", percentage: 80, color: "var(--primary-500)" },
    { subject: "Python", percentage: 75, color: "var(--warning-main)" },
    { subject: "Database Management", percentage: 65, color: "var(--success-main)" },
    { subject: "Operating Systems", percentage: 70, color: "var(--subj-os-text)" },
    { subject: "Artificial Intelligence", percentage: 85, color: "var(--subj-ai-text)" }
  ],

  recentSessions: [
    { subject: "Data Structures", duration: 45, type: "pomodoro", completedAgo: "5h ago" },
    { subject: "Python", duration: 60, type: "pomodoro", completedAgo: "2h ago" }
  ]
};
