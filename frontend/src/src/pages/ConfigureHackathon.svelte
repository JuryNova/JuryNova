<script>
  import toast from "svelte-french-toast";
  import ModalWrapper from "../components/ModalWrapper.svelte";
  import Nav from "../components/Nav.svelte";
  import axios from "axios";

  const BASEURL = import.meta.env.VITE_BASEURL;
  
  let loading = false;
  let data = { 
    theme: "", 
    technologies: "" 
  };

  async function handleSubmit() {
    if (!data.theme || !data.technologies) {
      toast.error("Please fill in all fields");
      return;
    }

    loading = true;
    try {
      const response = await axios.post(`${BASEURL}/create-hackathon`, data);
      if (response.data.message === "Hackathon created") {
        toast.success("Hackathon Configured Successfully");
        data = { theme: "", technologies: "" }; // Reset form
      } else {
        toast.error("Error creating hackathon");
      }
    } catch (error) {
      toast.error("Failed to create hackathon: " + error.message);
    } finally {
      loading = false;
    }
  }
</script>

<ModalWrapper>
  <div class="p-3 md:p-5 lg:p-10">
    <Nav />
    <main class="mt-16 mx-auto max-w-screen-md">
      <header class="flex gap-2 items-center mb-8">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-7 h-7"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        <h1 class="font-bold text-2xl">Configure Hackathon</h1>
      </header>

      <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <div class="form-control">
          <label for="theme" class="label">
            <span class="uppercase label-text-alt text-base font-bold opacity-50">
              What are the themes of the hackathon?
            </span>
          </label>
          <input
            id="theme"
            type="text"
            bind:value={data.theme}
            placeholder="Enter hackathon themes"
            class="input input-bordered w-full focus:ring-2 focus:ring-primary"
            required
          />
        </div>

        <div class="form-control">
          <label for="technologies" class="label">
            <span class="uppercase label-text-alt text-base font-bold opacity-50">
              List any required code libraries, dependencies, or APIs
            </span>
          </label>
          <input
            id="technologies"
            type="text"
            bind:value={data.technologies}
            placeholder="Enter required technologies"
            class="input input-bordered w-full focus:ring-2 focus:ring-primary"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary w-full sm:w-auto min-w-[150px] gap-2"
          disabled={loading}
        >
          {#if loading}
            <div class="loading loading-spinner" />
            <span>Configuring...</span>
          {:else}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
              />
            </svg>
            <span>Submit</span>
          {/if}
        </button>
      </form>
    </main>
  </div>
</ModalWrapper>