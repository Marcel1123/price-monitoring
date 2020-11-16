package drawers;

import entities.ProductEntity;
import lombok.Builder;
import lombok.Setter;

@Setter
@Builder
public class ProductDrawer {
    private ProductEntity productEntity;

    public void drawEvolutionGraphic(){

    }
}
