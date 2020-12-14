package page.classes.sliders;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import repositories.product.ProductRepository;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.inject.Inject;
import javax.inject.Named;

@Named
@RequestScoped
@Getter
@Setter
public class NumberOfFloorsSlider {
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    @Inject
    private ProductRepository productRepository;

    private int maximumNumberOfFloors;

    @PostConstruct
    public void init(){
        maximumNumberOfFloors = productRepository.getMaxNumberOfFloors();
    }
}
