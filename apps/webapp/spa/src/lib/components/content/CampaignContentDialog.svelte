<script lang="ts">
    import type { Content } from "$lib/api/content/Content";
    import InstagramPost from "$lib/components/content/instagram/InstagramPost.svelte";
    import LinkedInPost from "$lib/components/content/linkedin/LinkedInPost.svelte";
    import { Button } from "$lib/components/ui/button";
    import * as Dialog from "$lib/components/ui/dialog";
    import { Images } from "@lucide/svelte";
    import { X, Image, Type } from "lucide-svelte";

    type Props = {
        post: Content;
        open: Content | null;
        onClose?: () => void;
    };

    let { post, open, onClose }: Props = $props();

    let isOpen = $derived(!!open);

    const handleClose = () => {
        onClose?.();
    };

    const copyText = async () => {
        if (!post.caption) return;
        try {
            await navigator.clipboard.writeText(post.caption);
        } catch {
            //
        }
    };

    const copyImage = async () => {
        if (!post.mediaUrl) return;
        try {
            const response = await fetch(post.mediaUrl);
            const blob = await response.blob();
            await navigator.clipboard.write([
                new ClipboardItem({
                    [blob.type]: blob,
                }),
            ]);
        } catch {
            //
        }
    };

    const buttonStyle = "shadow-lg justify-start btn-rounded-full";
</script>

<Dialog.Root
    open={isOpen}
    onOpenChange={(newOpen) => !newOpen && handleClose()}
>
    <Dialog.Overlay class="bg-black/10 backdrop-blur-sm" />
    <Dialog.Content
        class="p-0 border-0 bg-transparent shadow-none"
        showCloseButton={false}
    >
        <div
            class="absolute top-4 -right-38 flex flex-col gap-2 z-10 items-start max-sm:hidden"
        >
            <Button variant="secondary" onclick={copyImage} class={buttonStyle}>
                <Images class="h-4 w-4" />
                Copy Image
            </Button>

            <Button variant="secondary" onclick={copyText} class={buttonStyle}>
                <Type class="h-4 w-4" />
                Copy Text
            </Button>

            <Button variant="ghost" onclick={handleClose} class={buttonStyle}>
                <X class="h-4 w-4" />
                Close
            </Button>
        </div>

        <div class="max-h-[90vh] overflow-y-auto">
            <div class="sm:hidden flex flex-row gap-2 justify-center mb-2">
                <Button
                    variant="secondary"
                    onclick={copyImage}
                    class={buttonStyle}
                >
                    <Image class="h-4 w-4" />
                </Button>

                <Button
                    variant="secondary"
                    onclick={copyText}
                    class={buttonStyle}
                >
                    <Type class="h-4 w-4" />
                </Button>

                <Button
                    variant="secondary"
                    onclick={handleClose}
                    class={buttonStyle}
                >
                    <X class="h-4 w-4" />
                </Button>
            </div>

            {#if post.channel === "INSTAGRAM"}
                <InstagramPost {post} />
            {:else if post.channel === "LINKEDIN"}
                <LinkedInPost {post} />
            {/if}
        </div>
    </Dialog.Content>
</Dialog.Root>
