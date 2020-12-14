package page.classes;

import util.enums.ProductType;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Named;

@Named
@ApplicationScoped
public class Data {

    public ProductType[] getStatuses() {
        return ProductType.values();
    }

}