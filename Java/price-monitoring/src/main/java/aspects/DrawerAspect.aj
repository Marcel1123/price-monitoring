package aspects;

public aspect DrawerAspect {
    pointcut productDrawer() : call(public void ProductDrawer.drawEvolutionGraphic());

    before() : productDrawer() {
        System.out.println("Start compute product information for display...");
    }

    after() : productDrawer() {
        System.out.println("End compute product information for display...");
    }

    pointcut categoryDrawer() : call(public void CategoryDrawer.drawEvolutionGraphic());

    before() : categoryDrawer() {
        System.out.println("Start compute category information for display...");
    }

    after() : categoryDrawer() {
        System.out.println("End compute category information for display...");
    }
}
