package page.classes.selectors;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import repositories.product.ProductRepository;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.inject.Inject;
import javax.inject.Named;
import java.util.List;

@Named
@RequestScoped
@Getter
@Setter
public class YearOfConstSelector {
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    @Inject
    private ProductRepository productRepository;

    private List<Integer> years;

    @PostConstruct
    public void init(){
        years = productRepository.getAllConstructYears();
    }
}
