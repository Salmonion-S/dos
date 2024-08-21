import asyncio
import aiohttp
import os
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn


console = Console()


async def checkpx(session, pxconc, progress, task_id, semaphore, goodpx):
    async with semaphore:
        pxraw = "\n".join(pxconc)
        data = pxraw.encode('utf-8')

        try:
            async with session.post("https://api3.natsumi.xyz/free", data=data) as response:
                json_response = await response.json()
                results = json_response['results']
                
                for r in results:
                    if r['status'] == 'working':
                        goodpx.add(f"{r['proxy']['host']}:{r['proxy']['port']}")

                working = len([r for r in results if r['status'] == 'working'])
                dead = len([r for r in results if r['status'] != 'working'])

                progress.update(task_id, advance=len(pxconc), description=f"[green]Working: {working}[/green] / [red]Dead: {dead}[/red]")

                return working, dead
        except Exception as e:
            console.print(f"[red]Error[/red]: {e}")
            return 0, 0

async def main(pxinput, pxoutput):
    os.system('cls' if os.name == 'nt' else 'clear')

    with open(pxinput, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    pxtotal = len(proxies)
    maxpxperrq = 1000
    concc = (pxtotal // maxpxperrq) + (1 if pxtotal % maxpxperrq != 0 else 0)
    working_total = 0
    dead_total = 0
    goodpx = set()

    console.print(f"[bold yellow]Fast & Simple Proxy Checker [/bold yellow]\n")
    console.print(f"Total Proxies Loaded: [blue]{pxtotal}[/blue]")
    console.print(f"Number of Batches: [blue]{concc}[/blue]\n")

    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("{task.completed}/{task.total} Proxies"),
    ) as progress:
        task_id = progress.add_task("[yellow]Checking Proxies...", total=pxtotal)

        semaphore = asyncio.Semaphore(100)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(concc):
                start = i * maxpxperrq
                end = start + maxpxperrq
                pxconc = proxies[start:end]

                tasks.append(checkpx(session, pxconc, progress, task_id, semaphore, goodpx))

            results = await asyncio.gather(*tasks)

            for working, dead in results:
                working_total += working
                dead_total += dead

    console.print("\n[bold]Checking Completed.[/bold]")
    console.print(f"Total Proxies: [blue]{pxtotal}[/blue]")
    console.print(f"Working Proxies: [green]{working_total}[/green]")
    console.print(f"Dead Proxies: [red]{dead_total}[/red]")
    console.print(f"[bold yellow]Note: working proxy above contains duplicated proxies. saved proxies to output alr removed dupe.[/bold yellow]\n")
    

    with open(pxoutput, 'w') as f:
        for proxy in goodpx:
            f.write(f"{proxy}\n")

if __name__ == "__main__":
    pxinput = input("Proxylist: ")
    pxoutput = input("Output: ")
    asyncio.run(main(pxinput, pxoutput))
