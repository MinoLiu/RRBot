from app import LOG
from app import utils
from app.rrbot import RRBot
from app.utils import War, Status, Work


class PoorBot(RRBot):
    async def __init__(self, **kwargs):
        await super().__init__(**kwargs)

    async def do_military_training(self) -> int:
        await self.click(War.selector(), War.military_training_selector())
        await self.click(War.military_training_selector(), War.send_ok_selector())
        await self.click(War.send_ok_selector(), utils.close_selector())
        await self.click(utils.close_selector())
        LOG.info("Military training complete")
        await self.sleep(2)
        return 3598

    async def do_work(self) -> int:
        await self.click(Work.selector(), ".imp.yellow.tip")

        soup = await self.get_soup()
        energy, energy_cooldown_time = Status.check_energy(soup)
        gold = Work.check_region_gold(soup)

        if not Work.can_work(soup):
            LOG.info("Working is not possible")
            return 600

        if gold > 0 and energy >= 10:
            self.click(Work.work_selector(), utils.close_selector())
            self.click(utils.close_selector())
            LOG.info("Mining complete, {} energys use to work".format(energy))
        elif gold > 0 and energy_cooldown_time == 0:
            self.click(Status.energy_bar_selector())
        else:
            if gold == 0:
                LOG.info("Region lack of gold")
                return 600
            elif energy >= 10 or energy_cooldown_time == 0:
                LOG.error("Some error occurred in mining")
                return 600
            return energy_cooldown_time

        return await self.do_work()

    async def idle(self):
        # work cooldown time
        work_c = 600

        war_c, is_traveling, _ = await self.check_overview()

        await self.do_perks_upgrade()

        if not is_traveling:
            await self.do_storage_supply()
            if war_c == 0:
                await self.do_military_training()
            work_c = await self.do_work()

        war_c, _, _ = await self.check_overview()
        perk_c = await self.calculate_perks_time()

        await self.sleep(min(perk_c, war_c, work_c))
