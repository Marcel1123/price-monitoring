package page.classes;

import util.enums.ProductType;

import javax.faces.bean.ApplicationScoped;
import javax.faces.bean.ManagedBean;

@ManagedBean
@ApplicationScoped
public class Data {

    public ProductType[] getStatuses() {
        return ProductType.values();
    }

}