package drawers;

import entities.LocationEntity;
import entities.ProductEntity;
import lombok.Builder;
import lombok.Setter;
import util.enums.ProductType;

import java.util.List;

@Setter
@Builder
public class CategoryDrawer {
    private List<ProductEntity> productList;

    private ProductType productType;

    private LocationEntity locationEntity;

    public void drawEvolutionGraphic(){

    }
}
