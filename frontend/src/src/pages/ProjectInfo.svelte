<script>
  // @ts-nocheck

  import Label from "../components/Label.svelte";
  import ModalWrapper from "../components/ModalWrapper.svelte";
  import Nav from "../components/Nav.svelte";
  import Typewriter from "svelte-typewriter";
  import { getRandomLoadingMessage } from "../store/loading";
  import axios from "axios";
  import { onMount } from "svelte";

  export let params = {};
  let usermessage = "";
  let chatbox;
  let scroll;
  let marketQuestion = [
    {
      question: "Who is the target audience of this idea?",
      title: "Target Audience",
    },
    {
      question: "What is the market size of this idea?",
      title: "Market Size",
    },
    { question: "What are the pitfalls of this idea?", title: "Pitfalls" },
    {
      question: "Are there any platforms like the idea, that already exist?",
      title: "Existing Platforms",
    },
    {
      question: "What is the potential of this idea?",
      title: "Potential",
    },
  ];
  let codeQuestion = [
    {
      question:
        "What are the technologies and programming language used in this project?",
      title: "Technologies",
    },
    {
      question: "Explain the project in brief",
      title: "Code Description",
    },
    {
      question: "How is the code quality of this project?",
      title: "Code Quality",
    },
    {
      question:
        "Does the project import and use any of the following dependencies/packages/APIs/libraries : ",
      title: "Potential",
    },
  ];
  let BASEURL = import.meta.env.VITE_BASEURL;
  async function dataload() {
    loading = true;
    const response = await axios.get(BASEURL + "/get-project/" + params.id);
    loading = false;
    data = response.data.project;
    data.marketAgentAnalysis = data.marketAgentAnalysis.map((item) => {
      return {
        question: marketQuestion.find((i) => {
          return i.question === item.question;
        }).title,
        answer: item.answer,
      };
    });
    data.codeAgentAnalysis = data.codeAgentAnalysis.map((item) => {
      let cq = codeQuestion.find((i) => {
        return i.question === item.question;
      });

      return {
        question: cq && "title" in cq ? cq.title : item.question,
        answer: item.answer,
      };
    });
  }
  onMount(async () => {
    dataload();
  });
  let data = {
    isReviewed: true,
    title: "JuryNova",
    longDescription: `Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam
      voluptatum, quibusdam, quia, quae voluptates dolorum quod
      voluptatibus quos quas voluptate quidem? Quisquam voluptatum,
      quibusdam, quia, quae voluptates dolorum quod voluptatibus quos
      quas voluptate quidem? Quisquam voluptatum, quibusdam, quia,
      quae voluptates dolorum quod voluptatibus quos quas voluptate
      quidem? Quisquam voluptatum, quibusdam, quia, quae voluptates
      dolorum quod voluptatibus quos quas voluptate quidem? Quisquam
      `,
    shortDescription: `Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam`,
    theme: "Healthcare",
    githubLink: "",
    demoLink: "",

    marketAgentAnalysis: [
      {
        question: "Target Audience",
        answer: `Lorem, ipsum dolor sit amet consectetur adipisicing elit. Numquam,
              esse debitis, assumenda rerum dignissimos illum iste asperiores
              cum veniam aut pariatur ipsam unde temporibus neque similique
              dolor molestiae enim libero?`,
      },
      {
        question: "Current Competition",
        answer: `Lorem, ipsum dolor sit amet consectetur adipisicing elit. Numquam,
              esse debitis, assumenda rerum dignissimos illum iste asperiores
              cum veniam aut pariatur ipsam unde temporibus neque similique
              dolor molestiae enim libero?`,
      },
    ],
    codeAgentAnalysis: [
      {
        question: "Target Audience",
        answer: `Lorem, ipsum dolor sit amet consectetur adipisicing elit. Numquam,
              esse debitis, assumenda rerum dignissimos illum iste asperiores
              cum veniam aut pariatur ipsam unde temporibus neque similique
              dolor molestiae enim libero?`,
      },
      {
        question: "Current Competition",
        answer: `Lorem, ipsum dolor sit amet consectetur adipisicing elit. Numquam,
              esse debitis, assumenda rerum dignissimos illum iste asperiores
              cum veniam aut pariatur ipsam unde temporibus neque similique
              dolor molestiae enim libero?`,
      },
    ],
  };
  let chat = [];
  let loading = false;
  let chatloading = false;

  async function toggleReview() {
    data.isReviewed = !data.isReviewed;
    const response = await axios.post(BASEURL + "/review", {
      project_id: params.id,
      isReviewed: data.isReviewed,
    });
  }
  let chathistory;
</script>

<ModalWrapper>
  <div class="p-3 md:p-5 lg:p-10">
    <Nav />
    {#if loading}
      <div class="flex flex-col gap-3 h-[80vh] justify-center items-center">
        <span class="loading loading-spinner loading-md" />
        <div class="max-w-xs text-sm text-center">
          {getRandomLoadingMessage()}
        </div>
      </div>
    {:else}
      <div class="grid md:grid-cols-4 mt-16 gap-7">
        <div class="flex flex-col">
          <div>
            <Label>Project Title</Label>
            <div class="text-4xl font-semibold">{data.title}</div>
          </div>

          <div class="mt-10">
            <Label>Project Description</Label>
            <div class="mt-1">
              {data.shortDescription}
            </div>
          </div>
          <div class="mt-10">
            <Label>Detailed Description</Label>
            <div class="mt-1">
              {data.longDescription}
            </div>
          </div>
          <div class="mt-10">
            <Label>Theme</Label>
            <div class="flex gap-3 justify-between items-center">
              {data.theme}
            </div>
          </div>
          <div class="mt-10">
            <Label>Project Links</Label>
            <div class="flex gap-3 items-center">
              {#if !data.githubLink && !data.demoLink}
                <div>No Links available</div>
              {/if}
              {#if data.githubLink}
                <button
                  on:click={() => (window.location.href = data.githubLink)}
                  class="btn btn-circle mt-3"
                  ><svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="black"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    class="w-6 h-6 text-black"
                    ><path
                      d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
                    /></svg
                  ></button
                >
              {/if}
              {#if data.demoLink}
                <button class="btn btn-circle mt-3"
                  ><svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-6 h-6"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5"
                    />
                  </svg>
                </button>
              {/if}
            </div>
          </div>
          <div class="mt-10">
            <Label>Actions</Label>
            <div class="flex gap-3 items-center mt-4">
              {#if data.isReviewed}
                <button class="btn" on:click={toggleReview}
                  ><svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-6 h-6"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>

                  Unreview</button
                >
              {:else}
                <button class="btn" on:click={toggleReview}
                  ><svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-6 h-6"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M4.5 12.75l6 6 9-13.5"
                    />
                  </svg>
                  Review</button
                >
              {/if}
            </div>
          </div>
        </div>
        <div class="flex flex-col">
          <div class="font-bold flex gap-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
              />
            </svg>

            <div>Market Analysis</div>
          </div>
          <div class="mt-7 flex-col flex gap-7">
            {#if "marketAgentAnalysis" in data}
              {#each data.marketAgentAnalysis as { question, answer }, index}
                <div>
                  <Label>
                    {question}</Label
                  >
                  <Typewriter
                    mode={"cascade"}
                    delay={index * 1000}
                    scrambleSlowdown={false}
                    interval={10}
                  >
                    {answer}
                  </Typewriter>
                </div>
              {/each}
            {:else}
              <div class="text-gray-500 animate-pulse">
                Generating Market Analysis
              </div>
            {/if}
          </div>
        </div>
        <div class="flex flex-col">
          <div class=" font-bold flex gap-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0021 18V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v12a2.25 2.25 0 002.25 2.25z"
              />
            </svg>

            <div>Code Analysis</div>
          </div>
          <div class="mt-7 flex-col flex gap-7">
            {#each data.codeAgentAnalysis as { question, answer }, index}
              <div>
                <Label>{question}</Label>
                <Typewriter
                  mode={"cascade"}
                  delay={index * 1000}
                  scrambleSlowdown={false}
                  interval={10}
                >
                  {answer}
                </Typewriter>
              </div>
            {/each}
          </div>
        </div>
        <div class="flex flex-col">
          <div class="font-bold flex gap-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"
              />
            </svg>

            <div>Chat with JuryNova</div>
          </div>
          <div
            bind:this={chatbox}
            class="flex flex-col bg-slate-50 p-4 my-4 mb-4 h-[500px] rounded-md overflow-auto"
          >
          
          {#if chat.length > 0}
            {#each chat as { output, input }}
              <div class="flex flex-col border-b py-2">
                <div class="font-bold text-sm tracking-wider text-slate-900">
                  You
                </div>
                <div class="flex items-center gap-2">
                  <div>{input}</div>
                  <button class="btn btn-circle btn-xs">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="flex flex-col border-b py-2">
                <div class="font-bold text-sm tracking-wider text-purple-500">
                  JuryNova
                </div>
                <div class="flex items-center gap-2">
                  <Typewriter class="">{output}</Typewriter>
                  <button class="btn btn-circle btn-xs">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
                    </svg>
                  </button>
                </div>
              </div>
            {/each}
          {/if}
          
            <div bind:this={scroll} id="scroll" />
          </div>
          <form
            on:submit|preventDefault={async () => {
              if (usermessage === "") return;
              if (chatloading) return;
              chatloading = true;
              const response = await axios.post(BASEURL + "/chat-agent", {
                question: usermessage,
                project_id: params.id,
                chathistory: chat,
              });
              chathistory = response.data.chathistory;
              chat = [{ input: usermessage, output: response.data.answer }];
              chatloading = false;
              usermessage = "";
              chatbox.scrollIntoView(true);
              scroll.scrollIntoView(true);
            }}
            class="join mb-5"
          >
            <input
              bind:value={usermessage}
              type="text"
              class="input input-bordered w-full join-item"
            />
            <button type="submit" disabled={chatloading} class="btn join-item">
              {#if chatloading}
                <div class="loading loading-spinner" />
              {:else}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="w-4 h-4"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25"
                  />
                </svg>
              {/if}
            </button>
          </form>
        </div>
      </div>
    {/if}
  </div>
</ModalWrapper>
