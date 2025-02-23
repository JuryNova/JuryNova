let loading = [
  "Loading creativity and innovation...",
  "Initializing judging algorithms...",
  "Compiling expertise and talent...",
  "Loading AI-powered judging modules...",
  "Processing submissions with lightning speed...",
  "Bringing the future of hackathons to your screen...",
  "Preparing to evaluate genius at its finest...",
  "Loading algorithms designed to spot the next big thing...",
  "Analyzing code and innovation in progress...",
  "Brace yourself for a revolutionary judging experience...",
];

// generate a random loading message
export function getRandomLoadingMessage() {
  return loading[Math.floor(Math.random() * loading.length)];
}
